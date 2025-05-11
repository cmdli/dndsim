import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { Character } from "../sim/Character"
import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { Feature } from "../sim/Feature"
import { applyFeatSchedule, defaultMagicBonus, rollDice } from "../util/helpers"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import {
    FinesseWeapon,
    SimpleWeapon,
    ThrownWeapon,
    Weapon,
} from "../sim/Weapon"
import { WeaponMastery } from "../sim/types"
import { Rapier } from "../weapons/martial/melee/Rapier"
import { IncreaseResource } from "../feats/shared/IncreaseResource"
import { SetAttribute } from "../feats/shared/SetAttribute"
import { Resource } from "../sim/resources/Resource"
import { ActionOperation } from "../sim/actions/ActionOperation"
import { Environment } from "../sim/Environment"
import { BoomingBlade } from "../spells/BoomingBlade"
import {
    AttackActionTag,
    DefaultAttackActionOperation,
    MainActionTag,
} from "../sim/actions/AttackAction"
import { NickAttackOperation } from "../sim/actions/NickAttackOperation"
import { Operation } from "../sim/actions/Operation"
import { Shortsword } from "../weapons/martial/melee/Shortsword"
import { Scimitar } from "../weapons/martial/melee/Scimitar"

const EnergyDieAttribute = "energyDie"
const EnergyDiceResource = "energyDice"
const SneakAttackTag = "SneakAttack"
const HomingStrikesTag = "HomingStrikes"

class SneakAttack extends Feature {
    used: boolean = false

    beginTurn(): void {
        this.used = false
    }

    attackResult(event: AttackResultEvent): void {
        const weapon = event.attack?.attack.weapon()
        if (weapon && event.hit && !this.used) {
            this.used = true
            const level = this.character.getClassLevel("Rogue")
            const diceCount = Math.ceil(level / 2)
            event.addDamage({
                source: "SneakAttack",
                dice: Array(diceCount).fill(6),
                type: weapon.damageType,
            })
            event.attack.addTag(SneakAttackTag)
        }
    }
}

class SteadyAim extends Feature {
    enabled: boolean = false

    beforeAction(): void {
        if (this.character.bonus.use(1, "SteadyAim")) {
            this.enabled = true
        }
    }

    attackRoll(event: AttackRollEvent): void {
        if (this.enabled) {
            event.adv = true
            this.enabled = false
        }
    }

    endTurn(): void {
        this.enabled = false
    }
}

class StrokeOfLuck extends Feature {
    used: boolean = false

    beginTurn(): void {
        this.used = false
    }

    attackRoll(event: AttackRollEvent): void {
        if (!this.used && !event.hits()) {
            this.used = true
            event.roll1 = 20
            event.roll2 = 20
        }
    }
}

class Assassinate extends Feature {
    firstTurn: boolean = true
    usedDmg: boolean = false
    adv: boolean = false

    constructor(private level: number) {
        super()
    }

    shortRest(): void {
        this.firstTurn = true
        this.usedDmg = false
    }

    beginTurn(): void {
        if (this.firstTurn) {
            // Simulate the initiative check
            const rogueRoll =
                Math.max(rollDice(1, 20), rollDice(1, 20)) +
                this.character.mod("dex")
            const enemyRoll = rollDice(1, 20)
            if (rogueRoll > enemyRoll) {
                this.adv = true
            }
        }
    }

    attackRoll(event: AttackRollEvent): void {
        if (this.adv) {
            event.adv = true
        }
    }

    attackResult(event: AttackResultEvent): void {
        const weapon = event.attack?.attack.weapon()
        if (
            weapon &&
            event.hit &&
            this.firstTurn &&
            !this.usedDmg &&
            event.attack.hasTag(SneakAttackTag)
        ) {
            this.usedDmg = true
            event.addDamage({
                source: "Assassinate",
                flatDmg: this.level,
                type: weapon.damageType,
            })
        }
    }

    endTurn(): void {
        this.adv = false
        this.firstTurn = false
    }
}

class DeathStrike extends Feature {
    enabled: boolean = false

    shortRest(): void {
        this.enabled = true
    }

    attackResult(event: AttackResultEvent): void {
        if (event.hit && this.enabled && event.attack.hasTag(SneakAttackTag)) {
            this.enabled = false
            if (!event.attack.target.save(this.character.dc("dex"))) {
                event.dmgMultiplier *= 2
            }
        }
    }

    endTurn(): void {
        this.enabled = false
    }
}

function psychicBlade({ isBonusAction = false } = {}): Weapon {
    return new Weapon({
        name: "Psychic Blade",
        mastery: "Vex",
        die: isBonusAction ? 4 : 6,
        damageType: "psychic",
        tags: [SimpleWeapon, ThrownWeapon, FinesseWeapon],
    })
}

class PsychicBladesBonusAction implements Operation {
    repeatable: boolean = false

    constructor(private psychicBlade: Weapon) {}

    eligible(environment: Environment, character: Character): boolean {
        return character.bonus.has()
    }

    do(environment: Environment, character: Character): void {
        character.bonus.use()
        character.weaponAttack({
            target: environment.target,
            weapon: this.psychicBlade,
            tags: ["bonus_action"],
        })
    }
}

class PsychicBladesAction extends ActionOperation {
    repeatable: boolean = false

    constructor(private psychicBlade: Weapon) {
        super()
    }

    action(environment: Environment): void {
        const target = environment.target
        const character = environment.character
        character.weaponAttack({
            target,
            weapon: this.psychicBlade,
            tags: [MainActionTag, AttackActionTag],
        })
    }
}

class PsychicBlades extends Feature {
    apply(character: Character): void {
        this.character.resources.set(
            EnergyDiceResource,
            new Resource({
                name: EnergyDiceResource,
                character: this.character,
                initialMax: 4,
                incrementOnShortRest: true,
                resetOnLongRest: true,
            })
        )
    }
}

class SoulBlades extends Feature {
    attackRoll(event: AttackRollEvent) {
        if (
            event.hits() ||
            event.isCritMiss() ||
            !this.character.hasResource(EnergyDiceResource)
        ) {
            return
        }

        event.situationalBonus += rollDice(
            1,
            this.character.getAttribute(EnergyDieAttribute)
        )
        event.attack.attack.addTag(HomingStrikesTag)

        this.character.useResource(EnergyDiceResource)
    }

    attackResult(event: AttackResultEvent) {
        // We consume it then restore it later on a miss so that we don't accidentally overspend
        if (!event.hit && event.attack.attack.hasTag(HomingStrikesTag)) {
            this.character.getResource(EnergyDiceResource).add(1)
        }
    }
}

class RendMind extends Feature {
    used: boolean = false

    longRest() {
        this.used = false
    }

    attackResult(event: AttackResultEvent) {
        const { target } = event.attack

        if (
            !event.hit ||
            !event.attack.hasTag(SneakAttackTag) ||
            target.hasCondition("stunned")
        ) {
            return
        }

        if (this.used && !this.character.hasResource(EnergyDiceResource, 3)) {
            return
        }

        if (!this.used) {
            this.used = true
        } else {
            this.character.useResource(EnergyDiceResource, 3)
        }

        if (!target.save(this.character.dc("dex"))) {
            target.addCondition("stunned")
            this.character.addTriggerEffect("begin_turn", (event) => {
                if (target.save(this.character.dc("dex"))) {
                    event.target.removeCondition("stunned")
                    return "stop"
                }
                return "continue"
            })
        }
    }
}

class BoomingBladeAction extends ActionOperation {
    repeatable: boolean = false
    constructor(private weapon: Weapon) {
        super()
    }

    action(environment: Environment): void {
        const spell = new BoomingBlade(this.weapon)
        environment.character.spells.cast({
            spell,
            target: environment.target,
        })
    }
}

export class Rogue {
    static baseFeatures(args: {
        level: number
        asis: Array<Feature>
        masteries: WeaponMastery[]
    }): Feature[] {
        const { level, asis, masteries } = args
        const features: Feature[] = []
        if (level >= 1) {
            features.push(new ClassLevel("Rogue", level))
            features.push(new SneakAttack())
            features.push(new WeaponMasteries(masteries))
        }
        // Level 2 (Cunning Action) is irrelevant for now
        if (level >= 3) {
            features.push(new SteadyAim())
        }
        // Level 5 (Cunning Strike) is mostly useless for DPR
        // Level 7 (Evasion) is irrelevant
        // Level 7 (Reliable Talent) is irrelevant
        // Level 11 (Improved Cunning Strike) is unused
        // Level 14 (Devious Strikes) is unused
        // Level 15 (Slippery Mind) is irrelevant
        // Level 18 (Elusive) is irrelevant
        if (level >= 20) {
            features.push(new StrokeOfLuck())
        }
        features.push(
            ...applyFeatSchedule({
                newFeats: asis,
                schedule: [4, 8, 10, 12, 16, 19],
                level,
            })
        )
        return features
    }

    static assassinFeatures(level: number): Feature[] {
        const features: Feature[] = []
        if (level >= 3) {
            features.push(new Assassinate(level))
        }
        // Level 3 (Assassin's Tools) is irrelevant
        // Level 9 (Infiltration Expertise) is irrelevant
        // TODO: Level 13 (Envenom Weapons)
        if (level >= 17) {
            features.push(new DeathStrike())
        }
        return features
    }

    static soulKnifeFeatures(level: number): Feature[] {
        const features: Feature[] = []
        if (level >= 3) {
            features.push(new PsychicBlades())
            features.push(new SetAttribute(EnergyDieAttribute, 6))
        }
        if (level >= 5) {
            features.push(new IncreaseResource(EnergyDiceResource, 2))
            features.push(new SetAttribute(EnergyDieAttribute, 8))
        }
        if (level >= 9) {
            features.push(new IncreaseResource(EnergyDiceResource, 2))
            features.push(new SoulBlades())
        }
        if (level >= 11) {
            features.push(new SetAttribute(EnergyDieAttribute, 10))
        }
        if (level >= 13) {
            features.push(new IncreaseResource(EnergyDiceResource, 2))
        }
        if (level >= 17) {
            features.push(new SetAttribute(EnergyDieAttribute, 12))
            features.push(new IncreaseResource(EnergyDiceResource, 2))
            features.push(new RendMind())
        }
        return features
    }

    static createAssassinRogue(
        level: number,
        useBoomingBlade: boolean = false
    ): Character {
        const magicBonus = defaultMagicBonus(level)
        const character = new Character({
            stats: { str: 10, dex: 17, con: 10, int: 10, wis: 10, cha: 10 },
        })
        let features: Feature[] = []
        if (level >= 5 && useBoomingBlade) {
            const rapier = new Rapier({ magicBonus })
            character.customTurn.addOperation(
                "action",
                new BoomingBladeAction(rapier)
            )
        } else {
            const shortsword = new Shortsword({
                magicBonus,
            })
            const scimitar = new Scimitar({
                magicBonus,
            })
            character.customTurn.addOperation(
                "action",
                new DefaultAttackActionOperation(shortsword)
            )
            character.customTurn.addOperation(
                "after_action",
                new NickAttackOperation(scimitar)
            )
        }
        features.push(
            ...Rogue.baseFeatures({
                level,
                masteries: ["Vex", "Nick"],
                asis: [
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex", "wis"),
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex"),
                    new IrresistibleOffense("dex"),
                ],
            })
        )
        features.push(...Rogue.assassinFeatures(level))
        features.forEach((feature) => character.addFeature(feature))
        return character
    }

    static createArcaneTricksterRogue(level: number): Character {
        const magicBonus = defaultMagicBonus(level)
        const character = new Character({
            stats: { str: 10, dex: 17, con: 10, int: 10, wis: 10, cha: 10 },
        })
        let features: Feature[] = []
        if (level >= 5) {
            const rapier = new Rapier({ magicBonus })
            character.customTurn.addOperation(
                "action",
                new BoomingBladeAction(rapier)
            )
        } else {
            const shortsword = new Shortsword({
                magicBonus,
            })
            const scimitar = new Scimitar({
                magicBonus,
            })
            character.customTurn.addOperation(
                "action",
                new DefaultAttackActionOperation(shortsword)
            )
            character.customTurn.addOperation(
                "after_action",
                new NickAttackOperation(scimitar)
            )
        }
        features = features.concat(
            Rogue.baseFeatures({
                level,
                masteries: ["Vex", "Nick"],
                asis: [
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex", "wis"),
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex"),
                    new IrresistibleOffense("dex"),
                ],
            })
        )
        // TODO: Arcane Trickster specific feats
        features.forEach((feature) => character.addFeature(feature))
        return character
    }

    static createSoulKnifeRogue(level: number): Character {
        const character = new Character({
            stats: { str: 10, dex: 17, con: 10, int: 10, wis: 10, cha: 10 },
        })
        let features: Feature[] = []
        // We begin using psychic blades once we reach level 3
        if (level < 3) {
            const shortsword = new Shortsword()
            const scimitar = new Scimitar()
            character.customTurn.addOperation(
                "action",
                new DefaultAttackActionOperation(shortsword)
            )
            character.customTurn.addOperation(
                "after_action",
                new NickAttackOperation(scimitar)
            )
        } else {
            character.customTurn.addOperation(
                "action",
                new PsychicBladesAction(psychicBlade())
            )
            character.customTurn.addOperation(
                "after_action",
                new PsychicBladesBonusAction(
                    psychicBlade({ isBonusAction: true })
                )
            )
        }
        features.push(
            ...Rogue.baseFeatures({
                level,
                masteries: ["Vex", "Nick"],
                asis: [
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex", "wis"),
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex"),
                    new IrresistibleOffense("dex"),
                ],
            })
        )
        features.push(...Rogue.soulKnifeFeatures(level))
        features.forEach((feature) => character.addFeature(feature))
        return character
    }
}

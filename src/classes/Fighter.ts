import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { ExtraAttack } from "../feats/shared/ExtraAttack"
import { GreatWeaponFighting } from "../feats/fightingStyle/GreatWeaponFighting"
import { GreatWeaponMaster } from "../feats/general/GreatWeaponMaster"
import { ImprovedCritical } from "../feats/shared/ImprovedCritical"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { Character } from "../sim/Character"
import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { BeginTurnEvent } from "../sim/events/BeginTurnEvent"
import { Feature } from "../sim/Feature"
import { WeaponMastery } from "../sim/types"
import { Weapon } from "../sim/Weapon"
import { applyFeatSchedule, defaultMagicBonus } from "../util/helpers"
import { SavageAttacker } from "../feats/origin/SavageAttacker"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { Environment } from "../sim/Environment"
import {
    AttackActionTag,
    MainActionTag,
    NumAttacksAttribute,
} from "../sim/actions/AttackAction"
import { Resource } from "../sim/resources/Resource"
import { Operation } from "../sim/actions/Operation"
import { ActionOperation } from "../sim/actions/ActionOperation"
import { Greatsword } from "../weapons/martial/melee/Greatsword"
import { Maul } from "../weapons/martial/melee/Maul"

const ActionSurgeResource = "ActionSurge"

class ActionSurgeOperation implements Operation {
    repeatable: boolean = false

    eligible(environment: Environment): boolean {
        return environment.character.hasResource(ActionSurgeResource)
    }

    do(environment: Environment): void {
        environment.character.useResource(ActionSurgeResource)
        environment.character.actions.add(1, true)
    }
}

class AddActionSurge extends Feature {
    apply(character: Character): void {
        if (!character.resources.has(ActionSurgeResource)) {
            character.resources.set(
                ActionSurgeResource,
                new Resource({
                    name: ActionSurgeResource,
                    character,
                    initialMax: 1,
                    resetOnShortRest: true,
                })
            )
        }
        character.getResource(ActionSurgeResource).addMax(1)
    }
}

class StudiedAttacks extends Feature {
    enabled: boolean = false

    attackRoll(event: AttackRollEvent): void {
        if (this.enabled) {
            event.adv = true
            this.enabled = false
        }
    }

    attackResult(event: AttackResultEvent): void {
        if (!event.hit) {
            this.enabled = true
        }
    }
}

class HeroicAdvantage extends Feature {
    used: boolean = false

    beginTurn(event: BeginTurnEvent): void {
        this.character.heroicInspiration.add(1)
    }

    attackRoll(event: AttackRollEvent): void {
        if (event.adv) {
            return
        }
        if (this.character.heroicInspiration.has()) {
            const roll = event.roll1
            if (roll < 8) {
                this.character.heroicInspiration.use()
                event.adv = true
            }
        }
    }
}

class PrecisionAttack extends Feature {
    low: number

    constructor(low: number) {
        super()
        this.low = low
    }

    attackRoll(event: AttackRollEvent): void {
        if (
            event.attack.hasTag("used_maneuver") ||
            !this.character.combatSuperiority.has() ||
            event.hits()
        ) {
            return
        }
        if (event.roll() >= this.low) {
            const roll = this.character.combatSuperiority.roll()
            event.situationalBonus += roll
            event.attack.addTag("used_maneuver")
        }
    }
}

// @ts-ignore
class TrippingAttack extends Feature {
    attackResult(event: AttackResultEvent): void {
        const weapon = event.attack?.attack.weapon()
        if (
            !weapon ||
            !event.hit ||
            event.attack.target.hasCondition("prone") ||
            event.attack.hasTag("used_maneuver") ||
            !this.character.combatSuperiority.has()
        ) {
            return
        }
        const roll = this.character.combatSuperiority.roll()
        event.addDamage({
            source: "TrippingAttack",
            dice: [roll],
            type: weapon.damageType,
        })
        if (!event.attack.target.save(this.character.dc("str"))) {
            event.attack.target.knockProne()
        }
    }
}

class CombatSuperiority extends Feature {
    level: number

    constructor(level: number) {
        super()
        this.level = level
    }

    apply(character: Character): void {
        let maxDice = 4
        if (this.level >= 15) {
            maxDice = 6
        } else if (this.level >= 7) {
            maxDice = 5
        }
        let die = 8
        if (this.level >= 18) {
            die = 12
        } else if (this.level >= 10) {
            die = 10
        }
        for (let i = 0; i < maxDice; i++) {
            character.combatSuperiority.addDie(die)
        }
    }
}

class Relentless extends Feature {
    apply(character: Character): void {
        character.combatSuperiority.enableRelentless()
    }
}

class ToppleIfNecessaryAttackAction extends ActionOperation {
    repeatable: boolean = true
    weapon: Weapon
    toppleWeapon: Weapon

    constructor(weapon: Weapon, toppleWeapon: Weapon) {
        super()
        this.weapon = weapon
        this.toppleWeapon = toppleWeapon
    }

    action(environment: Environment): void {
        const target = environment.target
        const character = environment.character
        const numAttacks = character.getAttribute(NumAttacksAttribute)
        for (let i = 0; i < numAttacks; i++) {
            let weapon = this.weapon
            if (!target.hasCondition("prone") && i < numAttacks - 1) {
                weapon = this.toppleWeapon
            }
            character.weaponAttack({
                target,
                weapon,
                tags: [MainActionTag, AttackActionTag],
            })
        }
    }
}

export class Fighter {
    static baseFeatures(args: {
        level: number
        asis: Array<Feature>
        masteries: WeaponMastery[]
        fightingStyle: Feature
    }): Feature[] {
        const { level, asis, masteries, fightingStyle } = args
        const features: Feature[] = []
        if (level >= 1) {
            features.push(new ClassLevel("Fighter", level))
            features.push(new WeaponMasteries(masteries))
            features.push(fightingStyle)
        }
        if (level >= 2) {
            features.push(new AddActionSurge())
        }
        if (level >= 5) {
            features.push(new ExtraAttack(2))
        }
        if (level >= 11) {
            features.push(new ExtraAttack(3))
        }
        if (level >= 13) {
            features.push(new StudiedAttacks())
        }
        if (level >= 17) {
            features.push(new AddActionSurge())
        }
        if (level >= 20) {
            features.push(new ExtraAttack(4))
        }
        features.push(
            ...applyFeatSchedule({
                newFeats: asis,
                schedule: [4, 6, 8, 12, 14, 16, 19],
                level,
            })
        )
        return features
    }

    static championFeatures(level: number): Feature[] {
        const features: Feature[] = []
        if (level >= 3) {
            features.push(new ImprovedCritical(19))
        }
        if (level >= 10) {
            features.push(new HeroicAdvantage())
        }
        if (level >= 15) {
            features.push(new ImprovedCritical(18))
        }
        return features
    }

    static battlemasterFeatures(level: number): Feature[] {
        const features: Feature[] = []
        if (level >= 3) {
            features.push(new CombatSuperiority(level))
        }
        if (level >= 15) {
            features.push(new Relentless())
        }
        return features
    }

    static createBattlemasterFighter(level: number): Character {
        const character = new Character({
            stats: { str: 17, dex: 10, con: 10, int: 10, wis: 10, cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })
        const toppleWeapon = new Maul({ magicBonus: defaultMagicBonus(level) })
        const features: Feature[] = []
        features.push(new SavageAttacker())
        features.push(
            ...Fighter.baseFeatures({
                level,
                asis: [
                    new GreatWeaponMaster(weapon),
                    new AbilityScoreImprovement("str"),
                    new AbilityScoreImprovement("con"),
                    new AbilityScoreImprovement("con"),
                    new AbilityScoreImprovement("con"),
                    new AbilityScoreImprovement("con"),
                    new IrresistibleOffense("str"),
                ],
                masteries: ["Topple", "Graze"],
                fightingStyle: new GreatWeaponFighting(),
            })
        )
        features.push(...Fighter.battlemasterFeatures(level))
        features.push(new PrecisionAttack(8))
        character.customTurn.addOperation(
            "before_action",
            new ActionSurgeOperation()
        )
        character.customTurn.addOperation(
            "action",
            new ToppleIfNecessaryAttackAction(weapon, toppleWeapon)
        )
        features.forEach((feature) => character.addFeature(feature))
        return character
    }

    static createChampionFighter(level: number): Character {
        const character = new Character({
            stats: { str: 17, dex: 10, con: 10, int: 10, wis: 10, cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })
        const toppleWeapon = new Maul({ magicBonus: defaultMagicBonus(level) })
        const features: Feature[] = []
        features.push(new SavageAttacker())
        features.push(
            ...Fighter.baseFeatures({
                level,
                asis: [
                    new GreatWeaponMaster(weapon),
                    new AbilityScoreImprovement("str"),
                    new AbilityScoreImprovement("con"),
                    new AbilityScoreImprovement("con"),
                    new AbilityScoreImprovement("con"),
                    new AbilityScoreImprovement("con"),
                    new IrresistibleOffense("str"),
                ],
                masteries: ["Graze", "Topple"],
                fightingStyle: new GreatWeaponFighting(),
            })
        )
        features.push(...Fighter.championFeatures(level))
        character.customTurn.addOperation(
            "before_action",
            new ActionSurgeOperation()
        )
        character.customTurn.addOperation(
            "action",
            new ToppleIfNecessaryAttackAction(weapon, toppleWeapon)
        )
        features.forEach((feature) => character.addFeature(feature))
        return character
    }
}

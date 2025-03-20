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
import { Feat } from "../sim/Feat"
import { WeaponMastery } from "../sim/types"
import { Weapon } from "../sim/Weapon"
import { applyFeatSchedule, defaultMagicBonus } from "../util/helpers"
import { SavageAttacker } from "../feats/origin/SavageAttacker"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { Greatsword } from "../weapons/index"
import { Maul } from "../weapons/index"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { Environment } from "../sim/Environment"
import { CustomTurn } from "../sim/steps/CustomTurn"
import {
    AttackActionStep,
    WeaponAttack,
} from "../sim/steps/core/AttackActionStep"
import { Resource } from "../sim/resources/Resource"
import { Step, TurnStage } from "../sim/steps/Step"

const ActionSurgeResource = "ActionSurge"

class ActionSurgeStep implements Step {
    stage(): TurnStage {
        return "before_action"
    }

    eligible(environment: Environment): boolean {
        return environment.character.resources.get(ActionSurgeResource)!.has()
    }

    do(environment: Environment): void {
        environment.character.resources.get(ActionSurgeResource)!.use()
        environment.character.actions.add(1, true)
    }

    repeatable(): boolean {
        return false
    }
}

class AddActionSurge extends Feat {
    apply(character: Character): void {
        let resource = character.resources.get(ActionSurgeResource)
        if (!resource) {
            resource = new Resource({
                name: ActionSurgeResource,
                character,
                initialMax: 1,
                resetOnShortRest: true,
            })
            character.resources.set(ActionSurgeResource, resource)
        }
        resource.addMax(1)
    }
}

class StudiedAttacks extends Feat {
    enabled: boolean = false

    apply(character: Character): void {
        character.events.on("attack_roll", (event) => this.attackRoll(event))
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
    }

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

class HeroicAdvantage extends Feat {
    used: boolean = false

    apply(character: Character): void {
        character.events.on("begin_turn", (event) => this.beginTurn(event))
        character.events.on("attack_roll", (event) => this.attackRoll(event))
    }

    beginTurn(event: BeginTurnEvent): void {
        this.character!.heroicInspiration.add(1)
    }

    attackRoll(event: AttackRollEvent): void {
        if (event.adv) {
            return
        }
        if (this.character!.heroicInspiration.has()) {
            const roll = event.roll1
            if (roll < 8) {
                this.character!.heroicInspiration.use()
                event.adv = true
            }
        }
    }
}

class PrecisionAttack extends Feat {
    low: number

    constructor(low: number) {
        super()
        this.low = low
    }

    apply(character: Character): void {
        character.events.on("attack_roll", (event) => this.attackRoll(event))
    }

    attackRoll(event: AttackRollEvent): void {
        if (
            event.attack.hasTag("used_maneuver") ||
            !this.character!.combatSuperiority.has() ||
            event.hits()
        ) {
            return
        }
        if (event.roll() >= this.low) {
            const roll = this.character!.combatSuperiority.roll()
            event.situationalBonus += roll
            event.attack.addTag("used_maneuver")
        }
    }
}

class TrippingAttack extends Feat {
    apply(character: Character): void {
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
    }

    attackResult(event: AttackResultEvent): void {
        if (
            !event.hit ||
            event.attack.target.prone ||
            event.attack.hasTag("used_maneuver") ||
            !this.character!.combatSuperiority.has()
        ) {
            return
        }
        const roll = this.character!.combatSuperiority.roll()
        event.addDamage({ source: "TrippingAttack", dice: [roll] })
        if (!event.attack.target.save(this.character!.dc("str"))) {
            event.attack.target.knockProne()
        }
    }
}

class CombatSuperiority extends Feat {
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

class Relentless extends Feat {
    apply(character: Character): void {
        character.combatSuperiority.enableRelentless()
    }
}

class ToppleWeaponAttack implements WeaponAttack {
    weapon: Weapon
    toppleWeapon: Weapon

    constructor(args: { weapon: Weapon; toppleWeapon: Weapon }) {
        this.weapon = args.weapon
        this.toppleWeapon = args.toppleWeapon
    }

    do(environment: Environment, character: Character): void {
        const target = environment.target
        let weapon = this.weapon
        if (!target.prone) {
            weapon = this.toppleWeapon
        }
        character.weaponAttack({
            target,
            weapon,
            tags: ["main_action"],
        })
    }
}

export class Fighter {
    static baseFeats(args: {
        level: number
        asis: Array<Feat>
        masteries: WeaponMastery[]
        fightingStyle: Feat
    }): Feat[] {
        const { level, asis, masteries, fightingStyle } = args
        const feats: Feat[] = []
        if (level >= 1) {
            feats.push(new ClassLevel("Fighter", level))
            feats.push(new WeaponMasteries(masteries))
            feats.push(fightingStyle)
        }
        if (level >= 2) {
            feats.push(new AddActionSurge())
        }
        if (level >= 5) {
            feats.push(new ExtraAttack(2))
        }
        if (level >= 11) {
            feats.push(new ExtraAttack(3))
        }
        if (level >= 13) {
            feats.push(new StudiedAttacks())
        }
        if (level >= 17) {
            feats.push(new AddActionSurge())
        }
        if (level >= 20) {
            feats.push(new ExtraAttack(4))
        }
        applyFeatSchedule({
            feats,
            newFeats: asis,
            schedule: [4, 6, 8, 12, 14, 16, 19],
            level,
        })
        return feats
    }

    static championFeats(level: number): Feat[] {
        const feats: Feat[] = []
        if (level >= 3) {
            feats.push(new ImprovedCritical(19))
        }
        if (level >= 10) {
            feats.push(new HeroicAdvantage())
        }
        if (level >= 15) {
            feats.push(new ImprovedCritical(18))
        }
        return feats
    }

    static battlemasterFeats(level: number): Feat[] {
        const feats: Feat[] = []
        if (level >= 3) {
            feats.push(new CombatSuperiority(level))
        }
        if (level >= 15) {
            feats.push(new Relentless())
        }
        return feats
    }

    static createBattlemasterFighter(level: number): Character {
        const character = new Character({
            stats: { str: 17, dex: 10, con: 10, int: 10, wis: 10, cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })
        const toppleWeapon = new Maul({ magicBonus: defaultMagicBonus(level) })
        const feats = []
        feats.push(new SavageAttacker())
        feats.push(
            ...Fighter.baseFeats({
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
        feats.push(...Fighter.battlemasterFeats(level))
        feats.push(new PrecisionAttack(8))
        character.customTurn = new CustomTurn([
            new ActionSurgeStep(),
            new AttackActionStep(
                new ToppleWeaponAttack({ weapon, toppleWeapon })
            ),
        ])
        feats.forEach((feat) => character.addFeat(feat))
        return character
    }

    static createChampionFighter(level: number): Character {
        const character = new Character({
            stats: { str: 17, dex: 10, con: 10, int: 10, wis: 10, cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })
        const toppleWeapon = new Maul({ magicBonus: defaultMagicBonus(level) })
        const feats = []
        feats.push(new SavageAttacker())
        feats.push(
            ...Fighter.baseFeats({
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
        feats.push(...Fighter.championFeats(level))
        character.customTurn = new CustomTurn([
            new ActionSurgeStep(),
            new AttackActionStep(
                new ToppleWeaponAttack({ weapon, toppleWeapon })
            ),
        ])
        feats.forEach((feat) => character.addFeat(feat))
        return character
    }
}

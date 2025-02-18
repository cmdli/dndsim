import { AbilityScoreImprovement } from "../feats/shared/AbilityScoreImprovement"
import { ExtraAttack } from "../feats/shared/ExtraAttack"
import { GreatWeaponFighting } from "../feats/fightingStyle/GreatWeaponFighting"
import { GreatWeaponMaster } from "../feats/GreatWeaponMaster"
import { ImprovedCritical } from "../feats/shared/ImprovedCritical"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { NumAttacksAttribute } from "../sim/actions/AttackAction"
import { Character } from "../sim/Character"
import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { ActionEvent } from "../sim/events/ActionEvent"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { BeginTurnEvent } from "../sim/events/BeginTurnEvent"
import { Feat } from "../sim/Feat"
import { WeaponMastery } from "../sim/types"
import { Weapon } from "../sim/Weapon"
import { applyFeatSchedule, defaultMagicBonus } from "../util/helpers"
import { Longsword } from "../weapons/Longsword"
import { SavageAttacker } from "../feats/origin/SavageAttacker"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { Greatsword } from "../weapons/Greatsword"
import { Maul } from "../weapons/Maul"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { ClassSchedule, FeatConfig, Schedule } from "../config/config"

class ActionSurge extends Feat {
    num: number = 0

    apply(character: Character): void {
        character.events.on("short_rest", () => this.onShortRest())
        character.events.on("before_action", () => this.onBeforeAction())
    }

    onShortRest() {
        this.num = this.character!.getAttribute("ActionSurgeMax")
    }

    onBeforeAction() {
        if (this.num > 0) {
            this.num -= 1
        }
    }
}

class ExtraActionSurge extends Feat {
    apply(character: Character): void {
        character.setAttribute(
            "ActionSurgeMax",
            character.getAttribute("ActionSurgeMax") + 1
        )
    }
}

class StudiedAttacks extends Feat {
    enabled: boolean = false

    apply(character: Character): void {
        character.events.on("attack_roll", (data) => {
            if (this.enabled) {
                data.adv = true
                this.enabled = false
            }
        })
        character.events.on("attack_result", (data) => {
            if (!data.hit) {
                this.enabled = true
            }
        })
    }
}

class HeroicAdvantage extends Feat {
    used: boolean = false

    apply(character: Character): void {
        character.events.on("begin_turn", (data) => this.beginTurn(data))
        character.events.on("attack_roll", (data) => this.attackRoll(data))
    }

    beginTurn(data: BeginTurnEvent): void {
        this.used = false
    }

    attackRoll(data: AttackRollEvent): void {
        if (this.used || data.adv) {
            return
        }
        const roll = data.roll1
        if (roll < 8) {
            this.used = true
            data.adv = true
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
        character.events.on("attack_roll", (data) => this.attackRoll(data))
    }

    attackRoll(data: AttackRollEvent): void {
        if (
            data.attack.hasTag("used_maneuver") ||
            !this.character!.combatSuperiority.has() ||
            data.hits()
        ) {
            return
        }
        if (data.roll() >= this.low) {
            const roll = this.character!.combatSuperiority.roll()
            data.situationalBonus += roll
            data.attack.addTag("used_maneuver")
        }
    }
}

class TrippingAttack extends Feat {
    apply(character: Character): void {
        character.events.on("attack_result", (data) => this.attackResult(data))
    }

    attackResult(data: AttackResultEvent): void {
        if (
            !data.hit ||
            data.attack.target.prone ||
            data.attack.hasTag("used_maneuver") ||
            !this.character!.combatSuperiority.has()
        ) {
            return
        }
        const roll = this.character!.combatSuperiority.roll()
        data.addDamage({ source: "TrippingAttack", dice: [roll] })
        if (!data.attack.target.save(this.character!.dc("str"))) {
            data.attack.target.knockProne()
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

export function fighterFeats(args: {
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
        feats.push(new ActionSurge())
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
        feats.push(new ExtraActionSurge())
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

export function championFeats(level: number): Feat[] {
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

export function battlemasterFeats(level: number): Feat[] {
    const feats: Feat[] = []
    if (level >= 3) {
        feats.push(new CombatSuperiority(level))
    }
    if (level >= 15) {
        feats.push(new Relentless())
    }
    return feats
}

class FighterAction extends Feat {
    weapon: Weapon
    toppleWeapon?: Weapon
    nickWeapon?: Weapon

    constructor(args: {
        weapon: Weapon
        toppleWeapon?: Weapon
        nickWeapon?: Weapon
    }) {
        super()
        this.weapon = args.weapon
        this.toppleWeapon = args.toppleWeapon
        this.nickWeapon = args.nickWeapon
    }

    apply(character: Character): void {
        character.events.on("action", (data) => this.action(data))
    }

    action(data: ActionEvent): void {
        const numAttacks =
            this.character?.getAttribute(NumAttacksAttribute) ?? 1
        for (let i = 0; i < numAttacks; i++) {
            let weapon = this.weapon
            if (this.toppleWeapon && !data.target.prone && i < numAttacks - 1) {
                weapon = this.toppleWeapon
            }
            this.character?.weaponAttack({
                target: data.target,
                weapon,
                tags: ["main_action"],
            })
        }
    }
}

export function createChampionFighter(level: number): Character {
    const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })
    const toppleWeapon = new Maul({ magicBonus: defaultMagicBonus(level) })
    const feats = []
    feats.push(new SavageAttacker())
    feats.push(
        ...fighterFeats({
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
    feats.push(...championFeats(level))
    feats.push(
        new FighterAction({
            weapon,
            toppleWeapon,
        })
    )
    return new Character({
        stats: {
            str: 17,
            dex: 10,
            con: 10,
            int: 10,
            wis: 10,
            cha: 10,
        },
        feats,
    })
}

export function createBattlemasterFighter(level: number): Character {
    const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })
    const feats = []
    feats.push(new SavageAttacker())
    feats.push(
        ...fighterFeats({
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
    feats.push(...battlemasterFeats(level))
    feats.push(new PrecisionAttack(8))
    feats.push(new FighterAction({ weapon }))
    return new Character({
        stats: { str: 17, dex: 10, con: 10, int: 10, wis: 10, cha: 10 },
        feats,
    })
}

function fighterSchedule(masteries: WeaponMastery[], fightingStyle: Feat) {
    return new ClassSchedule("Fighter", {
        1: new FeatConfig([new WeaponMasteries(masteries), fightingStyle]),
        2: new FeatConfig([new ActionSurge()]),
        5: new FeatConfig([new ExtraAttack(2)]),
        11: new FeatConfig([new ExtraAttack(3)]),
        13: new FeatConfig([new StudiedAttacks()]),
        17: new FeatConfig([new ExtraActionSurge()]),
        20: new FeatConfig([new ExtraAttack(4)]),
    })
}

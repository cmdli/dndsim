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

class ActionSurge extends Feat {
    num: number
    max: number

    constructor(max: number) {
        super()
        this.num = max
        this.max = max
    }

    apply(character: Character): void {
        character.events.on("short_rest", () => {
            this.num = this.max
        })
        character.events.on("before_action", () => {
            if (this.num > 0) {
                character.actions += 1
                this.num -= 1
            }
        })
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
        feats.push(new ActionSurge(level >= 17 ? 2 : 1))
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

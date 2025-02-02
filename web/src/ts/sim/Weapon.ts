import { Character } from "./Character"
import { AttackResultEvent } from "./events/AttackResultEvent"
import { DamageType, Stat, WeaponMastery } from "./types"

export type WeaponArgs = {
    name: string
    numDice: number
    die: number
    damageType?: DamageType
    minCrit?: number
    mastery?: WeaponMastery
    magicBonus?: number
    attackBonus?: number
    dmgBonus?: number
    tags?: Array<string>
}

export class Weapon {
    readonly name: string
    readonly numDice: number
    readonly die: number
    readonly damageType: DamageType
    readonly minCrit: number
    readonly mastery?: WeaponMastery
    readonly magicBonus: number
    readonly attackBonus: number
    readonly dmgBonus: number
    readonly tags: Set<string>

    constructor(args: WeaponArgs) {
        this.name = args.name
        this.numDice = args.numDice
        this.die = args.die
        this.damageType = args.damageType ?? "unknown"
        this.minCrit = args.minCrit ?? 20
        this.mastery = args.mastery
        this.magicBonus = args.magicBonus ?? 0
        this.attackBonus = args.attackBonus ?? 0
        this.dmgBonus = args.dmgBonus ?? 0
        this.tags = new Set(args.tags)
    }

    mod(character: Character): Stat {
        if (this.tags?.has("ranged")) {
            return "dex"
        } else if (
            this.tags?.has("finesse") &&
            character.stat("dex") > character.stat("str")
        ) {
            return "dex"
        } else {
            return "str"
        }
    }

    toHit(character: Character): number {
        return (
            character.prof() +
            character.mod(this.mod(character)) +
            this.attackBonus
        )
    }

    rolls(crit: boolean): Array<number> {
        let numDice = this.numDice
        if (crit) {
            numDice *= 2
        }
        return Array(numDice).fill(this.die)
    }

    attackResult(args: AttackResultEvent, character: Character): void {
        if (args.hit) {
            args.addDamage(this.name, this.rolls(args.crit), this.dmgBonus)
        }
    }
}

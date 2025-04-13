import { diceRolls } from "../../util/helpers"
import { DamageType } from "../types"

export class DamageRoll {
    source: string
    dice: Array<number>
    flatDmg: number
    type: DamageType
    rolls: Array<number>
    tags: Set<string>

    constructor(args: {
        source: string
        dice?: Array<number>
        flatDmg?: number
        type: DamageType
        tags?: Array<string>
    }) {
        this.source = args.source
        this.dice = args.dice ?? []
        this.flatDmg = args.flatDmg ?? 0
        this.type = args.type
        this.rolls = diceRolls(this.dice)
        this.tags = new Set(args.tags ?? [])
    }

    total(): number {
        return this.flatDmg + this.rolls.reduce((a, b) => a + b, 0)
    }

    replaceDice(dice: Array<number>): void {
        this.dice = dice
        this.reroll()
    }

    reroll(): void {
        this.rolls = diceRolls(this.dice)
    }

    addDice(dice: Array<number>): void {
        this.dice.push(...dice)
        const rolls = diceRolls(dice)
        this.rolls.push(...rolls)
    }

    hasTag(tag: string): boolean {
        return this.tags.has(tag)
    }
}

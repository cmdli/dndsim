import { diceRolls } from "../../util/helpers"
import { DamageType } from "../types"

export class DamageRoll {
    source: string
    dice: Array<number>
    flatDmg: number
    type: DamageType
    rolls: Array<number>

    constructor(args: {
        source: string
        dice?: Array<number>
        flatDmg?: number
        type: DamageType
    }) {
        this.source = args.source
        this.dice = args.dice ?? []
        this.flatDmg = args.flatDmg ?? 0
        this.type = args.type
        this.rolls = diceRolls(this.dice)
    }

    total(): number {
        return this.flatDmg + this.rolls.reduce((a, b) => a + b, 0)
    }

    reroll(): void {
        this.rolls = diceRolls(this.dice)
    }

    addDice(dice: Array<number>): void {
        this.dice.push(...dice)
        const rolls = diceRolls(dice)
        this.rolls.push(...rolls)
    }
}

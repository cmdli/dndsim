import { diceRolls } from "../../util/helpers"
import { rollDice } from "../../util/helpers"

export class DamageRoll {
    source: string
    dice: Array<number>
    flatDmg: number
    rolls: Array<number>
    constructor(args: {
        source: string
        dice?: Array<number>
        flatDmg?: number
    }) {
        this.source = args.source
        this.dice = args.dice ?? []
        this.flatDmg = args.flatDmg ?? 0
        this.rolls = diceRolls(this.dice)
    }

    total(): number {
        return this.flatDmg + rollDice(this.dice.length, this.dice[0])
    }

    reroll(): void {
        this.rolls = diceRolls(this.dice)
    }
}

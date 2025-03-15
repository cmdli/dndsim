import { diceRolls } from "../../util/helpers"

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
        return this.flatDmg + this.rolls.reduce((a, b) => a + b, 0)
    }

    reroll(): void {
        this.rolls = diceRolls(this.dice)
    }
}

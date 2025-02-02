import { rollDice } from "../util/helpers"

export class Target {
    prone: boolean = false
    ac: number
    damage: number = 0
    mod: number
    prof: number

    constructor(args: { ac: number; mod: number; prof: number }) {
        this.ac = args.ac
        this.mod = args.mod
        this.prof = args.prof
    }

    turn(): void {
        this.prone = false
    }

    knockProne(): void {
        this.prone = true
    }

    addDamage(amount: number): void {
        this.damage += amount
    }

    save(dc: number): boolean {
        return rollDice(1, 20) + this.mod + this.prof >= dc
    }
}

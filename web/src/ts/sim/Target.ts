import { profBonus, rollDice } from "../util/helpers"

const TARGET_AC = [
    13, // 1
    13, // 2
    13, // 3
    14, // 4
    15, // 5
    15, // 6
    15, // 7
    16, // 8
    16, // 9
    17, // 10
    17, // 11
    17, // 12
    18, // 13
    18, // 14
    18, // 15
    18, // 16
    19, // 17
    19, // 18
    19, // 19
    19, // 20
]

export class Target {
    ac: number
    mod: number
    prof: number

    prone: boolean = false
    stunned: boolean = false
    semistunned: boolean = false
    grappled: boolean = false
    damage: number = 0

    constructor(args: { level: number }) {
        this.ac = TARGET_AC[args.level - 1]
        if (args.level >= 8) {
            this.mod = 5
        } else if (args.level >= 4) {
            this.mod = 4
        } else {
            this.mod = 3
        }
        this.prof = profBonus(args.level)
    }

    longRest(): void {
        this.damage = 0
        this.shortRest()
    }

    shortRest(): void {
        this.stunned = false
        this.semistunned = false
        this.grappled = false
        this.prone = false
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

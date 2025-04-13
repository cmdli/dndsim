import { profBonus, rollDice } from "../util/helpers"
import { log } from "../util/Log"
import { Condition, DamageType } from "./types"

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

    damage: number = 0
    conditions: Map<Condition, number> = new Map()

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
        this.conditions.clear()
    }

    turn(): void {
        this.removeCondition("prone")
    }

    knockProne(): void {
        this.addCondition("prone")
    }

    grapple(): void {
        this.addCondition("grappled")
    }

    addDamage(source: string, type: DamageType, amount: number): void {
        log.record(`Damage (${source}, ${type})`, amount)
        this.damage += amount
    }

    save(dc: number): boolean {
        return rollDice(1, 20) + this.mod + this.prof >= dc
    }

    hasCondition(condition: Condition): boolean {
        return (this.conditions.get(condition) ?? 0) > 0
    }

    addCondition(condition: Condition): void {
        this.conditions.set(
            condition,
            (this.conditions.get(condition) ?? 0) + 1
        )
    }

    removeCondition(condition: Condition): void {
        const count = this.conditions.get(condition)
        if (count) {
            this.conditions.set(condition, count - 1)
        }
    }
}

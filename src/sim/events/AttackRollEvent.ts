import { rollDice } from "../../util/helpers"
import { AttackEvent } from "./AttackEvent"

export class AttackRollEvent {
    name: "attack_roll" = "attack_roll"
    attack: AttackEvent
    toHit: number
    adv: boolean = false
    disadv: boolean = false
    roll1: number = 0
    roll2: number = 0
    situationalBonus: number = 0
    minCrit: number
    autoHit: boolean = false

    constructor(args: { attack: AttackEvent; toHit: number }) {
        this.attack = args.attack
        this.toHit = args.toHit
        this.minCrit = args.attack.attack.minCrit()
        this.roll1 = rollDice(1, 20)
        this.roll2 = rollDice(1, 20)
    }

    reroll(): void {
        this.roll1 = rollDice(1, 20)
        this.roll2 = rollDice(1, 20)
    }

    roll(): number {
        if (this.adv && this.disadv) {
            return this.roll1
        }
        if (this.adv) {
            return Math.max(this.roll1, this.roll2)
        }
        if (this.disadv) {
            return Math.min(this.roll1, this.roll2)
        }
        return this.roll1
    }

    isCrit(): boolean {
        return this.roll() >= this.minCrit
    }

    isCritMiss(): boolean {
        return this.roll() === 1
    }

    hits(): boolean {
        if (this.autoHit || this.isCrit()) {
            return true
        }

        if (this.isCritMiss()) {
            return false
        }

        return (
            this.roll() + this.toHit + this.situationalBonus >=
            this.attack.target.ac
        )
    }
}

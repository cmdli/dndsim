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
    minCrit?: number
    private tags: Set<String> = new Set()

    constructor(args: { attack: AttackEvent; toHit: number }) {
        this.attack = args.attack
        this.toHit = args.toHit
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

    hits(): boolean {
        return (
            this.roll() + this.toHit + this.situationalBonus >=
            this.attack.target.ac
        )
    }

    addTag(name: string) {
        this.tags.add(name)
    }

    hasTag(name: string): boolean {
        return this.tags.has(name)
    }
}

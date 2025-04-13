import { rollDice } from "../../util/helpers"
import { Character } from "../Character"

export class CombatSuperiority {
    character: Character
    relentlessEnabled: boolean
    maxDice: number[]
    dice: number[]

    constructor(character: Character) {
        this.character = character
        this.relentlessEnabled = false
        this.maxDice = []
        this.dice = []

        this.character.events.on("short_rest", () => this.reset())
        this.character.events.on("long_rest", () => this.reset())
    }

    enableRelentless(): void {
        this.relentlessEnabled = true
    }

    addDie(die: number): void {
        this.maxDice.push(die)
    }

    reset(): void {
        this.dice = Array.from(this.maxDice)
    }

    use(): number {
        if (this.dice.length > 0) {
            return this.dice.shift()!
        }
        if (this.relentlessEnabled) {
            return 8
        }
        return 0
    }

    has(): boolean {
        return this.relentlessEnabled || this.dice.length > 0
    }

    roll(): number {
        const die = this.use()
        if (die === 0) {
            return 0
        }
        return rollDice(1, die)
    }
}

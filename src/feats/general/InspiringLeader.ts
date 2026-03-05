import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class InspiringLeader extends Feature {
    constructor(private stat: "Wis" | "Cha") {
        super()
    }

    apply(character: Character): void {
        // Temp hitpoints are untracked
        character.increaseStatMax(this.stat, 1)
    }
}

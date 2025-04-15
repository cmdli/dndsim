import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class InspiringLeader extends Feat {
    constructor(private stat: "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // Temp hitpoints are untracked
        character.increaseStatMax(this.stat, 1)
    }
}

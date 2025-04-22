import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"
import { Stat } from "../../sim/types"

export class Resilient extends Feature {
    constructor(private stat: Stat) {
        super()
    }

    apply(character: Character): void {
        // Saving throws aren't tracked
        character.increaseStat(this.stat, 1)
    }
}

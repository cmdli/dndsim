import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"
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

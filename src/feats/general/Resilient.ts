import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Resilient extends Feat {
    constructor(private stat: Stat) {
        super()
    }

    apply(character: Character): void {
        // Saving throws aren't tracked
        character.increaseStat(this.stat, 1)
    }
}

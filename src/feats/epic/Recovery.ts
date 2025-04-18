import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

// Mostly a no-op since hit points are ignored
export class Recovery extends Feat {
    constructor(private stat: Stat) {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
        character.increaseStat(this.stat, 1)
    }
}

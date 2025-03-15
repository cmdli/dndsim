import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

// Mostly a no-op since hit points are ignored
export class Recovery extends Feat {
    stat: Stat

    constructor(stat: Stat) {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
        character.increaseStat(this.stat, 1)
    }
}

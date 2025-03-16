import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class DualWielder extends Feat {
    stat: "str" | "dex"

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // TODO: Figure out how to do the extra bonus action attack
        // without it being required in the turn setup
        character.increaseStat(this.stat, 1)
    }
}

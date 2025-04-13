import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Sentinel extends Feat {
    stat: Stat

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Reaction attacks aren't tracked
        character.increaseStat(this.stat, 1)
    }
}

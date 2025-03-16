import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Athlete extends Feat {
    stat: Stat

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        // Movement is not tracked in the sim,
        // so the other benefits are not valuable
    }
}

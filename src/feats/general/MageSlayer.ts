import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class MageSlayer extends Feat {
    stat: Stat

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Target's don't cast spells so this is mostly empty
        character.increaseStat(this.stat, 1)
    }
}

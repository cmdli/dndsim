import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

// Ignoring the offensive benefits since they require
// Dim light and the opponent to not have truesight or blindsight,
// which is relatively situational at level 19+.
export class NightSpirit extends Feat {
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

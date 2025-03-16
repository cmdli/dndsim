import { Character } from "../../main"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class SkillExpert extends Feat {
    stat: Stat

    constructor(stat: Stat) {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Skills are not tracked
        character.increaseStat(this.stat, 1)
    }
}

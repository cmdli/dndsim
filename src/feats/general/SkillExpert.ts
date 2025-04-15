import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class SkillExpert extends Feat {
    constructor(private stat: Stat) {
        super()
    }

    apply(character: Character): void {
        // Skills are not tracked
        character.increaseStat(this.stat, 1)
    }
}

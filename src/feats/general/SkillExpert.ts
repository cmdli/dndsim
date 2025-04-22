import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"
import { Stat } from "../../sim/types"

export class SkillExpert extends Feature {
    constructor(private stat: Stat) {
        super()
    }

    apply(character: Character): void {
        // Skills are not tracked
        character.increaseStat(this.stat, 1)
    }
}

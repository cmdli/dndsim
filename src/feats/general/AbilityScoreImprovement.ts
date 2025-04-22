import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"
import { Stat } from "../../sim/types"

export class AbilityScoreImprovement extends Feature {
    constructor(private mod1: Stat, private mod2?: Stat) {
        super()
    }

    apply(character: Character): void {
        if (this.mod2) {
            character.increaseStat(this.mod1, 1)
            character.increaseStat(this.mod2, 1)
        } else {
            character.increaseStat(this.mod1, 2)
        }
    }
}

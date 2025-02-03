import { Character } from "../sim/Character"
import { Feat } from "../sim/Feat"
import { Stat } from "../sim/types"

export class AbilityScoreImprovement extends Feat {
    private mod1: Stat
    private mod2?: Stat
    constructor(mod1: Stat, mod2?: Stat) {
        super()
        this.mod1 = mod1
        this.mod2 = mod2
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

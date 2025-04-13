import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class InspiringLeader extends Feat {
    stat: Stat

    constructor(stat: "wis" | "cha") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Temp hitpoints are untracked
        character.increaseStatMax(this.stat, 1)
    }
}

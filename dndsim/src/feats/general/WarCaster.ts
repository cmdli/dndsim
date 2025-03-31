import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class WarCaster extends Feat {
    stat: Stat

    constructor(stat: "int" | "wis" | "cha") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Opportunity attacks and concentration is not used
        character.increaseStat(this.stat, 1)
    }
}

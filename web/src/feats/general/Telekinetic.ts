import { Character } from "../../main"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Telekinetic extends Feat {
    stat: Stat

    constructor(stat: "int" | "wis" | "cha") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Positioning is not tracked,
        // so the shove isn't useful
        character.increaseStat(this.stat, 1)
    }
}

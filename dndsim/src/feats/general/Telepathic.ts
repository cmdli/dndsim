import { Character } from "../../main"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Telepathic extends Feat {
    stat: Stat

    constructor(stat: "int" | "wis" | "cha") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Detect thoughts is useless
        character.increaseStat(this.stat, 1)
    }
}

import { Character } from "../../main"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class HeavilyArmored extends Feat {
    stat: Stat = "con"

    constructor(stat: "str" | "con") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
    }
}

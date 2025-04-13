import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class FeyTouched extends Feat {
    stat: "int" | "wis" | "cha"

    constructor(stat: "int" | "wis" | "cha") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        // TODO: Track extra spell resource here
    }
}

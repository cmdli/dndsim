import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class FeyTouched extends Feat {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        // TODO: Track extra spell resource here
    }
}

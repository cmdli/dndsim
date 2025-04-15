import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Telepathic extends Feat {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // Detect thoughts is useless
        character.increaseStat(this.stat, 1)
    }
}

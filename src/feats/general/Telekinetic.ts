import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Telekinetic extends Feat {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // Positioning is not tracked,
        // so the shove isn't useful
        character.increaseStat(this.stat, 1)
    }
}

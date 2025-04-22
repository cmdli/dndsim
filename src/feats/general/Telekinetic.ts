import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Telekinetic extends Feature {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // Positioning is not tracked,
        // so the shove isn't useful
        character.increaseStat(this.stat, 1)
    }
}

import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Telepathic extends Feature {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // Detect thoughts is useless
        character.increaseStat(this.stat, 1)
    }
}

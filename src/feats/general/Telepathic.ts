import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Telepathic extends Feature {
    constructor(private stat: "Int" | "Wis" | "Cha") {
        super()
    }

    apply(character: Character): void {
        // Detect thoughts is useless
        character.increaseStat(this.stat, 1)
    }
}

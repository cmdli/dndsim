import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class FeyTouched extends Feature {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        // TODO: Track extra spell resource here
    }
}

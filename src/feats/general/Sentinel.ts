import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Sentinel extends Feature {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Reaction attacks aren't tracked
        character.increaseStat(this.stat, 1)
    }
}

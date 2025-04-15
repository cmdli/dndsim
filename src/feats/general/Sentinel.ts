import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Sentinel extends Feat {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Reaction attacks aren't tracked
        character.increaseStat(this.stat, 1)
    }
}

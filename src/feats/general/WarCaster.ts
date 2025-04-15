import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class WarCaster extends Feat {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // Opportunity attacks and concentration is not used
        character.increaseStat(this.stat, 1)
    }
}

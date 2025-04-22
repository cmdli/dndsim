import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class WarCaster extends Feature {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // Opportunity attacks and concentration is not used
        character.increaseStat(this.stat, 1)
    }
}

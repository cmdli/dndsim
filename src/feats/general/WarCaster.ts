import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class WarCaster extends Feature {
    constructor(private stat: "Int" | "Wis" | "Cha") {
        super()
    }

    apply(character: Character): void {
        // Opportunity attacks and concentration is not used
        character.increaseStat(this.stat, 1)
    }
}

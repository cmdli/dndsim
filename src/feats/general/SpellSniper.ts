import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class SpellSniper extends Feature {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // Other benefits are not used
        character.increaseStat(this.stat, 1)
    }
}

import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class SpellSniper extends Feat {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // Other benefits are not used
        character.increaseStat(this.stat, 1)
    }
}

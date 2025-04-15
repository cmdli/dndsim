import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class HeavilyArmored extends Feat {
    constructor(private stat: "str" | "con") {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
    }
}

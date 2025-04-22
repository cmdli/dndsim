import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class HeavilyArmored extends Feature {
    constructor(private stat: "str" | "con") {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
    }
}

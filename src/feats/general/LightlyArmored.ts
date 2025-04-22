import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class LightlyArmored extends Feature {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
    }
}

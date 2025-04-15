import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class LightlyArmored extends Feat {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
    }
}

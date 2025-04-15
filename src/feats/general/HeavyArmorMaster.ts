import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class HeavyArmorMaster extends Feat {
    constructor(private stat: "str" | "con") {
        super()
    }

    apply(character: Character): void {
        // We don't track hit points so damage reduction is unused
        character.increaseStatMax(this.stat, 1)
    }
}

import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class HeavyArmorMaster extends Feature {
    constructor(private stat: "Str" | "Con") {
        super()
    }

    apply(character: Character): void {
        // We don't track hit points so damage reduction is unused
        character.increaseStatMax(this.stat, 1)
    }
}

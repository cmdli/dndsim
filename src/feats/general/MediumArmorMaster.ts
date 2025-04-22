import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class MediumArmorMaster extends Feature {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Character AC is untracked
        character.increaseStat(this.stat, 1)
    }
}

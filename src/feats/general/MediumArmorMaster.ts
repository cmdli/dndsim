import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class MediumArmorMaster extends Feat {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Character AC is untracked
        character.increaseStat(this.stat, 1)
    }
}

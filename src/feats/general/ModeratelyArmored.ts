import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class ModeratelyArmored extends Feat {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Armor proficiency is untracked
        character.increaseStat(this.stat, 1)
    }
}

import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class ModeratelyArmored extends Feature {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Armor proficiency is untracked
        character.increaseStat(this.stat, 1)
    }
}

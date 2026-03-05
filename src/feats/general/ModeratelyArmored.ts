import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class ModeratelyArmored extends Feature {
    constructor(private stat: "Str" | "Dex") {
        super()
    }

    apply(character: Character): void {
        // Armor proficiency is untracked
        character.increaseStat(this.stat, 1)
    }
}

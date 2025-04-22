import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class MageSlayer extends Feature {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Target's don't cast spells so this is mostly empty
        character.increaseStat(this.stat, 1)
    }
}

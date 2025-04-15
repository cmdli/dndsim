import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Observant extends Feat {
    constructor(private stat: "int" | "wis") {
        super()
    }

    apply(character: Character): void {
        // Both search action and skills are untracked
        character.increaseStat(this.stat, 1)
    }
}

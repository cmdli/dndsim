import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Observant extends Feature {
    constructor(private stat: "Int" | "Wis") {
        super()
    }

    apply(character: Character): void {
        // Both search action and skills are untracked
        character.increaseStat(this.stat, 1)
    }
}

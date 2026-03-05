import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class RitualCaster extends Feature {
    constructor(private stat: "Int" | "Wis" | "Cha") {
        super()
    }

    apply(character: Character): void {
        // TODO: Track spell availability
        // However, rituals aren't all that useful for damage
        character.increaseStat(this.stat, 1)
    }
}

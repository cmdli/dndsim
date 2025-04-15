import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class RitualCaster extends Feat {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // TODO: Track spell availability
        // However, rituals aren't all that useful for damage
        character.increaseStat(this.stat, 1)
    }
}

import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class RitualCaster extends Feat {
    stat: Stat

    constructor(stat: "int" | "wis" | "cha") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // TODO: Track spell availability
        // However, rituals aren't all that useful for damage
        character.increaseStat(this.stat, 1)
    }
}

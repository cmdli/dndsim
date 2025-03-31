import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Observant extends Feat {
    stat: Stat

    constructor(stat: "int" | "wis") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Both search action and skills are untracked
        character.increaseStat(this.stat, 1)
    }
}

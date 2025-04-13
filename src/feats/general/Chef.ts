import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

// Hit points are not tracked so this is mostly a no-op
export class Chef extends Feat {
    stat: Stat

    constructor(stat: "con" | "wis") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
    }
}

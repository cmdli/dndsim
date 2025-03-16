import { Character } from "../../main"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class MountedCombatant extends Feat {
    stat: Stat

    constructor(stat: "str" | "dex" | "wis") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
    }
}

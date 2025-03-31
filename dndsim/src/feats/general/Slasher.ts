import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Slasher extends Feat {
    stat: Stat

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Target movement and attack rolls are not used,
        // so this feat doesn't do anything extra
        character.increaseStat(this.stat, 1)
    }
}

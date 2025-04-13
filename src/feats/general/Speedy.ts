import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Speedy extends Feat {
    stat: Stat

    constructor(stat: "dex" | "con") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Movement and opportunity attacks are not used
        character.increaseStat(this.stat, 1)
    }
}

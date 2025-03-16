import { Character } from "../../main"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class ModeratelyArmored extends Feat {
    stat: Stat

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Armor proficiency is untracked
        character.increaseStat(this.stat, 1)
    }
}

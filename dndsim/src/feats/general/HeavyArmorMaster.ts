import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class HeavyArmorMaster extends Feat {
    stat: Stat

    constructor(stat: "str" | "con") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // We don't track hit points so damage reduction is unused
        character.increaseStatMax(this.stat, 1)
    }
}

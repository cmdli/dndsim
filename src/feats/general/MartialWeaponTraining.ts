import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class MartialWeaponTraining extends Feat {
    stat: Stat

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // Weapon proficiency is untracked
        character.increaseStat(this.stat, 1)
    }
}

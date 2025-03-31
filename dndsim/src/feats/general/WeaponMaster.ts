import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat, WeaponMastery } from "../../sim/types"

export class WeaponMaster extends Feat {
    stat: Stat
    mastery: WeaponMastery
    constructor(stat: "str" | "dex", mastery: WeaponMastery) {
        super()
        this.stat = stat
        this.mastery = mastery
    }

    apply(character: Character): void {
        // Skills are not tracked
        character.increaseStat(this.stat, 1)
        character.masteries.add(this.mastery)
    }
}

import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { WeaponMastery } from "../../sim/types"

export class WeaponMaster extends Feat {
    constructor(private stat: "str" | "dex", private mastery: WeaponMastery) {
        super()
    }

    apply(character: Character): void {
        // Skills are not tracked
        character.increaseStat(this.stat, 1)
        character.masteries.add(this.mastery)
    }
}

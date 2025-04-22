import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"
import { WeaponMastery } from "../../sim/types"

export class WeaponMaster extends Feature {
    constructor(private stat: "str" | "dex", private mastery: WeaponMastery) {
        super()
    }

    apply(character: Character): void {
        // Skills are not tracked
        character.increaseStat(this.stat, 1)
        character.masteries.add(this.mastery)
    }
}

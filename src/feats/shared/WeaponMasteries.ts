import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"
import { WeaponMastery } from "../../sim/types"

export class WeaponMasteries extends Feature {
    masteries: WeaponMastery[]

    constructor(masteries: WeaponMastery[]) {
        super()
        this.masteries = masteries
    }

    apply(character: Character): void {
        this.masteries.forEach((mastery) => character.masteries.add(mastery))
    }
}

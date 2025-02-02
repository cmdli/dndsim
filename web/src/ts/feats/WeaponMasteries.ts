import { Character } from "../sim/Character"
import { Feat } from "../sim/Feat"
import { WeaponMastery } from "../sim/types"

export class WeaponMasteries extends Feat {
    masteries: WeaponMastery[]

    constructor(masteries: WeaponMastery[]) {
        super()
        this.masteries = masteries
    }

    apply(character: Character): void {
        this.masteries.forEach((mastery) => character.masteries.add(mastery))
    }
}

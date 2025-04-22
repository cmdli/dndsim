import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class MartialWeaponTraining extends Feature {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Weapon proficiency is untracked
        character.increaseStat(this.stat, 1)
    }
}

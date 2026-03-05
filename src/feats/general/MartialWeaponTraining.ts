import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class MartialWeaponTraining extends Feature {
    constructor(private stat: "Str" | "Dex") {
        super()
    }

    apply(character: Character): void {
        // Weapon proficiency is untracked
        character.increaseStat(this.stat, 1)
    }
}

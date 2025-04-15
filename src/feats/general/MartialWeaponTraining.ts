import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class MartialWeaponTraining extends Feat {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Weapon proficiency is untracked
        character.increaseStat(this.stat, 1)
    }
}

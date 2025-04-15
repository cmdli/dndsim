import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class MountedCombatant extends Feat {
    constructor(private stat: "str" | "dex" | "wis") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
    }
}

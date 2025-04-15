import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class ShadowTouched extends Feat {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // TODO: Track spell availability
        character.increaseStat(this.stat, 1)
    }
}

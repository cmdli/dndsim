import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class ShadowTouched extends Feature {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        // TODO: Track spell availability
        character.increaseStat(this.stat, 1)
    }
}

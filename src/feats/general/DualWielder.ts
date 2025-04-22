import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class DualWielder extends Feature {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // TODO: Figure out how to do the extra bonus action attack
        // without it being required in the turn setup
        character.increaseStat(this.stat, 1)
    }
}

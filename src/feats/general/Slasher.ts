import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Slasher extends Feature {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Target movement and attack rolls are not used,
        // so this feat doesn't do anything extra
        character.increaseStat(this.stat, 1)
    }
}

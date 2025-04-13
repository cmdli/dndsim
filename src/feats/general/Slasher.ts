import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Slasher extends Feat {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // Target movement and attack rolls are not used,
        // so this feat doesn't do anything extra
        character.increaseStat(this.stat, 1)
    }
}

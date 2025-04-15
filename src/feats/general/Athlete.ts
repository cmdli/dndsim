import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Athlete extends Feat {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        // Movement is not tracked in the sim,
        // so the other benefits are not valuable
    }
}

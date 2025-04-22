import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Athlete extends Feature {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        // Movement is not tracked in the sim,
        // so the other benefits are not valuable
    }
}

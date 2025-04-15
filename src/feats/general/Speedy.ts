import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Speedy extends Feat {
    constructor(private stat: "dex" | "con") {
        super()
    }

    apply(character: Character): void {
        // Movement and opportunity attacks are not used
        character.increaseStat(this.stat, 1)
    }
}

import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Speedy extends Feature {
    constructor(private stat: "Dex" | "Con") {
        super()
    }

    apply(character: Character): void {
        // Movement and opportunity attacks are not used
        character.increaseStat(this.stat, 1)
    }
}

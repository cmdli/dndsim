import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

// Hit points are not tracked so this is mostly a no-op
export class Chef extends Feat {
    constructor(private stat: "con" | "wis") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
    }
}

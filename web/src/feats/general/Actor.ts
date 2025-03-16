import { Character } from "../../main"
import { Feat } from "../../sim/Feat"

export class Actor extends Feat {
    apply(character: Character): void {
        character.increaseStat("cha", 1)
        // Other benefits are non-mechanical in this sim
    }
}

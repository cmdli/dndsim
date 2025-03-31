import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Durable extends Feat {
    apply(character: Character): void {
        // We ignore death saving throws
        // and hit points
        character.increaseStat("con", 1)
    }
}

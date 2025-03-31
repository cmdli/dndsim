import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class KeenMind extends Feat {
    apply(character: Character): void {
        // Both skills and the Study action are unused
        character.increaseStatMax("int", 1)
    }
}

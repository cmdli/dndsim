import { Character } from "../../main"
import { Feat } from "../../sim/Feat"

export class Musician extends Feat {
    apply(character: Character): void {
        character.heroicInspiration.resetOnShortRest = true
    }
}

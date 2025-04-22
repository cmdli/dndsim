import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class Musician extends Feature {
    apply(character: Character): void {
        character.heroicInspiration.resetOnShortRest = true
    }
}

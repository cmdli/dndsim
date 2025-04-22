import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Musician extends Feature {
    apply(character: Character): void {
        character.heroicInspiration.resetOnShortRest = true
    }
}

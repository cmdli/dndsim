import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class KeenMind extends Feature {
    apply(character: Character): void {
        // Both skills and the Study action are unused
        character.increaseStatMax("int", 1)
    }
}

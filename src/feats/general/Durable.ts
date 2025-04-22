import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Durable extends Feature {
    apply(character: Character): void {
        // We ignore death saving throws
        // and hit points
        character.increaseStat("con", 1)
    }
}

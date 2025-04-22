import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class Actor extends Feature {
    apply(character: Character): void {
        character.increaseStat("cha", 1)
        // Other benefits are non-mechanical in this sim
    }
}

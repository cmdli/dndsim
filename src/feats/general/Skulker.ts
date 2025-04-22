import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class Skulker extends Feature {
    apply(character: Character): void {
        // Stealth and blindsight are not used
        character.increaseStat("dex", 1)
    }
}

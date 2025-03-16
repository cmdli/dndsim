import { Character } from "../../main"
import { Feat } from "../../sim/Feat"

export class Skulker extends Feat {
    apply(character: Character): void {
        // Stealth and blindsight are not used
        character.increaseStat("dex", 1)
    }
}

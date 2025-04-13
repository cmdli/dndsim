import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Sharpshooter extends Feat {
    apply(character: Character): void {
        // Other benefits aren't tracked
        character.increaseStat("dex", 1)
    }
}

import { Character } from "../../main"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Sharpshooter extends Feat {
    apply(character: Character): void {
        // Other benefits aren't tracked
        character.increaseStat("dex", 1)
    }
}

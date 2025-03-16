import { Character } from "../../main"
import { Feat } from "../../sim/Feat"

export class DefensiveDuelist extends Feat {
    apply(character: Character): void {
        // AC Reaction is ignored here
        character.increaseStat("dex", 1)
    }
}

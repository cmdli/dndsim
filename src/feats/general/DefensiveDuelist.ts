import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class DefensiveDuelist extends Feature {
    apply(character: Character): void {
        // AC Reaction is ignored here
        character.increaseStat("dex", 1)
    }
}

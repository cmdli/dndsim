import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Sharpshooter extends Feature {
    apply(character: Character): void {
        // Other benefits aren't tracked
        character.increaseStat("dex", 1)
    }
}

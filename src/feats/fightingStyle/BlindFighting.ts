import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class BlindFighting extends Feature {
    // No-op
    apply(character: Character): void {}
}

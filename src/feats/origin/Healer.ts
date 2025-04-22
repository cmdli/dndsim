import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class Healer extends Feature {
    // No-op
    apply(character: Character): void {}
}

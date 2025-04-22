import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Healer extends Feature {
    // No-op
    apply(character: Character): void {}
}

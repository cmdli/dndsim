import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Tough extends Feature {
    // No-op since we don't track hit points
    apply(character: Character): void {}
}

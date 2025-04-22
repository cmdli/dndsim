import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Interception extends Feature {
    // No-op since we have no allies
    apply(character: Character): void {}
}

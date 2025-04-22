import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class Protection extends Feature {
    // No-op since we have no allies
    apply(character: Character): void {}
}

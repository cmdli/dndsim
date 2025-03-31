import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Protection extends Feat {
    // No-op since we have no allies
    apply(character: Character): void {}
}

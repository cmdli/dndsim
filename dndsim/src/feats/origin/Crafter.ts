import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Crafter extends Feat {
    // No-op
    apply(character: Character): void {}
}

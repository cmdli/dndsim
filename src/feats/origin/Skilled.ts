import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class Skilled extends Feat {
    // No-op
    apply(character: Character): void {}
}

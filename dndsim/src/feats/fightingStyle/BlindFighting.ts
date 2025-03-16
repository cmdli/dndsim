import { Character } from "../../main"
import { Feat } from "../../sim/Feat"

export class BlindFighting extends Feat {
    // No-op
    apply(character: Character): void {}
}

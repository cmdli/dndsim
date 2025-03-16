import { Character } from "../../main"
import { Feat } from "../../sim/Feat"

export class Crafter extends Feat {
    // No-op
    apply(character: Character): void {}
}

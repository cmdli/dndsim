import { Character } from "../../main"
import { Feat } from "../../sim/Feat"

export class Tough extends Feat {
    // No-op since we don't track hit points
    apply(character: Character): void {}
}

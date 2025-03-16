import { Character } from "../../main"
import { Feat } from "../../sim/Feat"

export class MagicInitiate extends Feat {
    // No-op since we really don't track spells
    // TODO: Track level 1 spell usage and cantrips
    apply(character: Character): void {}
}

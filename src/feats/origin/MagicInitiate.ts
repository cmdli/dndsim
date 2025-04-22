import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class MagicInitiate extends Feature {
    // No-op since we really don't track spells
    // TODO: Track level 1 spell usage and cantrips
    apply(character: Character): void {}
}

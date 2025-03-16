import { Character } from "../../main"
import { Feat } from "../../sim/Feat"

export class Alert extends Feat {
    // No-Op feat since we don't have initiative
    apply(character: Character): void {}
}

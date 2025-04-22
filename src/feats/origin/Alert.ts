import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class Alert extends Feature {
    // No-Op feat since we don't have initiative
    apply(character: Character): void {}
}

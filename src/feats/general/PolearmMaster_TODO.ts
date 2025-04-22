import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class PolearmMaster extends Feature {
    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        // We ignore the reaction attack from PAM
        // TODO: Figure out how to handle the bonus action attack
        character.increaseStat(this.stat, 1)
    }
}

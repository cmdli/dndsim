import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class PolearmMaster extends Feat {
    stat: Stat

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // We ignore the reaction attack from PAM
        // TODO: Figure out how to handle the bonus action attack
        character.increaseStat(this.stat, 1)
    }
}

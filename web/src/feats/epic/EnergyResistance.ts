import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

// We are ignoring energy redirection for now
export class EnergyResistance extends Feat {
    stat: Stat

    constructor(stat: Stat) {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
        character.increaseStat(this.stat, 1)
    }
}

import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"
import { Stat } from "../../sim/types"

// We are ignoring energy redirection for now
export class EnergyResistance extends Feature {
    constructor(private stat: Stat) {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
        character.increaseStat(this.stat, 1)
    }
}

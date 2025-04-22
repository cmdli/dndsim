import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class MountedCombatant extends Feature {
    constructor(private stat: "str" | "dex" | "wis") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
    }
}

import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class MountedCombatant extends Feature {
    constructor(private stat: "Str" | "Dex" | "Wis") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
    }
}

import { Character } from "../../sim/Character"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feature } from "../../sim/Feature"

export class ElementalAdept extends Feature {
    constructor(
        private stat: "int" | "wis" | "cha",
        private damageType: "acid" | "cold" | "fire" | "lightning" | "thunder"
    ) {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
    }

    damageRoll(event: DamageRollEvent): void {
        if (event.damage.type != this.damageType) {
            return
        }

        for (let i = 0; i < event.damage.rolls.length; i++) {
            if (event.damage.rolls[i] === 1) {
                event.damage.rolls[i] = 2
            }
        }
    }
}

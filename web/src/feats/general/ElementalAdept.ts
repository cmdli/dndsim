import { Character } from "../../main"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feat } from "../../sim/Feat"

export class ElementalAdept extends Feat {
    stat: "int" | "wis" | "cha"
    damageType: "acid" | "cold" | "fire" | "lightning" | "poison"

    constructor(
        stat: "int" | "wis" | "cha",
        damageType: "acid" | "cold" | "fire" | "lightning" | "poison"
    ) {
        super()
        this.stat = stat
        this.damageType = damageType
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        character.events.on("damage_roll", (event) => this.damageRoll(event))
    }

    damageRoll(event: DamageRollEvent): void {
        // TODO: Turn 1's into 2's here
        // This is so minor and tracking damage types
        // isn't implemented yet, so I'm just not gonna do it
    }
}

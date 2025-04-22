import { Character } from "../../sim/Character"
import { CastSpellEvent } from "../../sim/events/CastSpellEvent"
import { Feature } from "../../sim/Feature"
import { rollDice } from "../../util/helpers"

export class SpellRecall extends Feature {
    constructor(private stat: "int" | "wis" | "cha") {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
        character.increaseStat(this.stat, 1)
    }

    castSpell(event: CastSpellEvent): void {
        if (event.spell.slot > 0 && event.spell.slot <= 4) {
            if (rollDice(1, 4) === event.spell.slot) {
                this.character.spells.addSlot(event.spell.slot)
            }
        }
    }
}

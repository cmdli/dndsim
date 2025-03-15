import { Character } from "../../sim/Character"
import { CastSpellEvent } from "../../sim/events/CastSpellEvent"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"
import { rollDice } from "../../util/helpers"

export class SpellRecall extends Feat {
    stat: Stat

    constructor(stat: "int" | "wis" | "cha") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
        character.increaseStat(this.stat, 1)
    }

    castSpell(event: CastSpellEvent): void {
        if (event.spell.slot > 0 && event.spell.slot <= 4) {
            if (rollDice(1, 4) === event.spell.slot) {
                this.character?.spells.addSlot(event.spell.slot)
            }
        }
    }
}

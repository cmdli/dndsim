import { Feature } from "../Feature"
import { Character } from "../Character"
import { Spellcaster } from "./shared"
import { Stat } from "../types"

export class SpellcastingFeat extends Feature {
    constructor(
        private stat: Stat,
        private spellcaster: Spellcaster,
        private level: number
    ) {
        super()
    }

    apply(character: Character): void {
        character.spells.setMod(this.stat)
        character.spells.addSpellcasterLevel(this.spellcaster, this.level)
    }
}

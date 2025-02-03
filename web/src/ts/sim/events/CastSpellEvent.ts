import { Spell } from "../spells/Spell"
import { CharacterEvent } from "./CharacterEvent"

export class CastSpellEvent extends CharacterEvent {
    name: "cast_spell" = "cast_spell"
    spell: Spell

    constructor(args: { spell: Spell }) {
        super()
        this.spell = args.spell
    }
}

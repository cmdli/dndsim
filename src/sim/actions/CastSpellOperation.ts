import { Character } from "../Character"
import { Environment } from "../Environment"
import { Spell } from "../spells/Spell"
import { Operation } from "./Operation"

export class CastSpellOperation implements Operation {
    repeatable = false

    constructor(private spellConstructor: () => Spell) {}

    eligible(environment: Environment, character: Character): boolean {
        const spell = this.spellConstructor()
        if (spell.castingTime === "bonus_action") {
            return character.bonus.has()
        } else if (spell.castingTime === "action") {
            return character.actions.has()
        }
        return false
    }

    do(environment: Environment, character: Character): void {
        const spell = this.spellConstructor()
        if (spell.castingTime === "bonus_action") {
            character.bonus.use()
        } else if (spell.castingTime === "action") {
            character.actions.use()
        }
        character.spells.cast({ spell, target: environment.target })
    }
}

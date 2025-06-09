import { Character } from "../sim/Character"
import { Environment } from "../sim/Environment"
import { Spell } from "../sim/spells/Spell"
import { Operation } from "../sim/actions/Operation"

export class CastSpellOperation implements Operation {
    repeatable = false

    constructor(
        protected spellConstructor: (character: Character) => Spell | undefined
    ) {}

    eligible(environment: Environment, character: Character): boolean {
        const spell = this.spellConstructor(character)
        if (!spell) {
            return false
        }
        if (spell.castingTime === "bonus_action" && !character.bonus.has()) {
            return false
        } else if (spell.castingTime === "action" && !character.actions.has()) {
            return false
        }
        if (spell.slot > 0 && !character.spells.hasSpellSlot(spell.slot)) {
            return false
        }
        return true
    }

    do(environment: Environment, character: Character): void {
        const spell = this.spellConstructor(character)
        if (!spell) {
            return
        }
        if (spell.castingTime === "bonus_action") {
            character.bonus.use()
        } else if (spell.castingTime === "action") {
            character.actions.use()
        }
        character.spells.cast({ spell, target: environment.target })
    }
}

export class CastSpellIfNecessaryOperation extends CastSpellOperation {
    constructor(spellConstructor: (character: Character) => Spell | undefined) {
        super(spellConstructor)
    }

    eligible(environment: Environment, character: Character): boolean {
        if (!super.eligible(environment, character)) {
            return false
        }
        const spell = this.spellConstructor(character)
        return !!spell && !character.hasEffect(spell.name)
    }
}

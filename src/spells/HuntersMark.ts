import { Character } from "../sim/Character"
import {
    ConcentrationSpell,
    ConcentrationSpellEffect,
} from "../sim/spells/Spell"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { EffectDuration } from "../sim/Effect"

class HuntersMarkEffect extends ConcentrationSpellEffect {
    duration: EffectDuration = "until_short_rest"

    apply(character: Character): void {
        super.apply(character)
        character.events.on("attack_result", this.attackResult)
    }

    end(character: Character): void {
        super.end(character)
        character.events.removeListener("attack_result", this.attackResult)
    }

    attackResult = (event: AttackResultEvent): void => {
        const weapon = event.attack?.attack.weapon()
        if (event.hit && weapon && this.character.hasEffect("HuntersMark")) {
            event.addDamage({
                source: this.name,
                dice: [6],
                type: weapon.damageType,
            })
        }
    }
}

export class HuntersMark extends ConcentrationSpell {
    constructor(slot?: number) {
        super({
            name: "HuntersMark",
            slot: slot || 1,
            concentration: true,
            castingTime: "bonus_action",
        })
    }

    effect(): HuntersMarkEffect {
        return new HuntersMarkEffect(this.name)
    }
}

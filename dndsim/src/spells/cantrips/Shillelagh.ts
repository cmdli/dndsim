import { Club, Quarterstaff } from "../../weapons";
import { SpellcastingSchool } from "../../sim/spells/shared";
import { Spell } from "../../sim/spells/Spell";
import { Character } from "../../sim/Character";
import { BeforeAttackEvent } from "../../sim/events/BeforeAttackEvent";
import { AttackResultEvent } from "../../sim/events/AttackResultEvent";

const ShillelaghEffect = 'Shillelagh'

export class Shillelagh extends Spell<Club | Quarterstaff> {
    constructor() {
        super({
            name: "Shillelagh",
            level: 0,
            duration: 10,
            school: SpellcastingSchool.Transmutation,
        })
    }

    cast(character: Character, target: Club | Quarterstaff) {
        super.cast(character)
        target.addEffect(ShillelaghEffect)

        character.events.on("before_attack", (event) => this.beforeAttack(event))
        character.events.on("attack_result", (event) => this.attackResult(event))
    }

    beforeAttack(event: BeforeAttackEvent) {
        if (event.attackEvent.attack.weapon()?.hasEffect(ShillelaghEffect)) {
            event.attackEvent.attack.addStat(this.character.spells.stat)
            // TODO: Set that the damage type can be replaced with force
        }
    }

    attackResult(event: AttackResultEvent) {
        const weapon = event.attack?.attack.weapon()

        if (!weapon?.hasEffect(ShillelaghEffect)) {
            return
        }

        event.damageRolls
            .filter((damageRoll) => damageRoll.hasTag("base_weapon_damage"))
            .forEach((damageRoll) => damageRoll.maybeReplaceDice(this.dice()))
    }

    dice(): number[] {
        switch (this.character.cantripTier()) {
            case 1:
                return [8]
            case 2:
                return [10]
            case 3:
                return [12]
            case 4:
                return [6, 6]
        }
    }
}
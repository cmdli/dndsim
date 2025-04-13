import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { BaseWeaponDamageTag, UnarmedWeapon } from "../../sim/Weapon"

export class UnarmedFighting extends Feat {
    apply(character: Character): void {
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
    }

    attackResult(event: AttackResultEvent) {
        const weapon = event.attack?.attack.weapon()
        if (!weapon?.hasTag(UnarmedWeapon)) {
            return
        }

        // The die should be reduced to a d6 while holding any weapons or a shield
        event.damageRolls
            .filter((damageRoll) => damageRoll.hasTag(BaseWeaponDamageTag))
            .forEach((damageRoll) => {
                if (damageRoll.dice.length == 0) {
                    // It must be doing a base 1 damage. Replace it with the d8
                    damageRoll.addDice([8])
                    damageRoll.flatDmg -= 1
                } else {
                    damageRoll.replaceDice(
                        damageRoll.dice.map((die) => Math.max(die, 8))
                    )
                }
            })
    }
}

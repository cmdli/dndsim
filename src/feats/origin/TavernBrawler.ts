import { BaseWeaponDamageTag, UnarmedWeapon } from "../../sim/Weapon"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feature } from "../../sim/Feature"
import { rollDice } from "../../util/helpers"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"

export class TavernBrawler extends Feature {
    attackResult(event: AttackResultEvent) {
        const weapon = event.attack?.attack.weapon()
        if (!weapon?.hasTag(UnarmedWeapon)) {
            return
        }

        event.damageRolls
            .filter((damageRoll) => damageRoll.hasTag(BaseWeaponDamageTag))
            .forEach((damageRoll) => {
                if (damageRoll.dice.length == 0) {
                    // It must be doing a base 1 damage. Replace it with the d4
                    damageRoll.addDice([4])
                    damageRoll.flatDmg -= 1
                } else {
                    damageRoll.replaceDice(
                        damageRoll.dice.map((die) => Math.max(die, 4))
                    )
                }
            })
    }

    damageRoll(args: DamageRollEvent): void {
        for (let i = 0; i < args.damage.rolls.length; i++) {
            if (args.damage.rolls[i] === 1) {
                args.damage.rolls[i] = rollDice(1, args.damage.dice[i])
            }
        }
    }
}

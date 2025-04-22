import { Character } from "../../sim/Character"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feature } from "../../sim/Feature"
import { TwoHandedWeapon } from "../../sim/Weapon"
import { log } from "../../util/Log"

export class GreatWeaponFighting extends Feature {
    apply(character: Character): void {
        character.events.on("damage_roll", (data) => this.damageRoll(data))
    }

    damageRoll(args: DamageRollEvent): void {
        const weapon = args.attack?.attack.weapon()
        if (weapon && weapon.hasTag(TwoHandedWeapon)) {
            for (let i = 0; i < args.damage.rolls.length; i++) {
                if (args.damage.rolls[i] === 1 || args.damage.rolls[i] === 2) {
                    log.record(
                        `Great Weapon Fighting (${weapon.name})`,
                        args.damage.rolls[i]
                    )
                    args.damage.rolls[i] = 3
                }
            }
        }
    }
}

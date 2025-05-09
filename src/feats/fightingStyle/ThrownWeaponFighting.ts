import { Character } from "../../sim/Character"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feature } from "../../sim/Feature"

export class ThrownWeaponFighting extends Feature {
    apply(character: Character): void {
        character.events.on("damage_roll", (event) => this.damageRoll(event))
    }

    damageRoll(event: DamageRollEvent) {
        const weapon = event.attack?.attack.weapon()
        if (
            weapon &&
            weapon.hasTag("thrown") &&
            event.attack?.attack.isRanged()
        ) {
            event.damage.flatDmg += 2
        }
    }
}

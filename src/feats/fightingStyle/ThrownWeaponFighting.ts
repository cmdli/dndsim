import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feature } from "../../sim/Feature"

export class ThrownWeaponFighting extends Feature {
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

import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feature } from "../../sim/Feature"
import { TwoHandedWeapon } from "../../sim/Weapon"

export class Dueling extends Feature {
    damageRoll(event: DamageRollEvent) {
        // Just assume that this is the only weapon if we are taking this feat
        if (!event.attack?.attack.hasTag(TwoHandedWeapon)) {
            event.damage.flatDmg += 2
        }
    }
}

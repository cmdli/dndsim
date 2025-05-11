import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feature } from "../../sim/Feature"
import { RangedWeapon } from "../../sim/Weapon"

export class Archery extends Feature {
    attackRoll(event: AttackRollEvent) {
        if (event.attack.attack.weapon()?.hasTag(RangedWeapon)) {
            event.situationalBonus += 2
        }
    }
}

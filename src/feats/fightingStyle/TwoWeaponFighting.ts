import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feature } from "../../sim/Feature"

export class TwoWeaponFighting extends Feature {
    attackRoll(event: AttackRollEvent) {
        if (event.attack.hasTag("light")) {
            event.attack.removeTag("light")
        }
    }
}

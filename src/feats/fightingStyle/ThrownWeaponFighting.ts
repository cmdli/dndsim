import { Character } from "../../sim/Character"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feat } from "../../sim/Feat"

export class ThrownWeaponFighting extends Feat {
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

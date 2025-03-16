import { Character } from "../../main"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feat } from "../../sim/Feat"
import { UnarmedWeapon } from "../../sim/Weapon"

export class UnarmedFighting extends Feat {
    apply(character: Character): void {
        character.events.on("damage_roll", (event) => this.damageRoll(event))
    }

    damageRoll(event: DamageRollEvent) {
        if (event.attack?.attack.weapon()?.hasTag(UnarmedWeapon)) {
            event.damage.addDice([8])
            // Subtract 1 since unarmed strikes are normally 1 + Str
            event.damage.flatDmg -= 1
        }
    }
}

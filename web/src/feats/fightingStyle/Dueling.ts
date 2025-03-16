import { Character } from "../../main"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feat } from "../../sim/Feat"
import { TwoHandedWeapon } from "../../sim/Weapon"

export class Dueling extends Feat {
    apply(character: Character): void {
        character.events.on("damage_roll", (event) => this.damageRoll(event))
    }

    damageRoll(event: DamageRollEvent) {
        // Just assume that this is the only weapon if we are taking this feat
        if (!event.attack?.attack.hasTag(TwoHandedWeapon)) {
            event.damage.flatDmg += 2
        }
    }
}

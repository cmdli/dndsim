import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feature } from "../../sim/Feat"
import { RangedWeapon } from "../../sim/Weapon"

export class Archery extends Feature {
    apply(character: Character): void {
        character.events.on("attack_roll", (event) => this.attackRoll(event))
    }

    attackRoll(event: AttackRollEvent) {
        if (event.attack.attack.weapon()?.hasTag(RangedWeapon)) {
            event.situationalBonus += 2
        }
    }
}

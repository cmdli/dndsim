import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feat } from "../../sim/Feat"

export class TwoWeaponFighting extends Feat {
    apply(character: Character): void {
        character.events.on("attack_roll", (event) => this.attackRoll(event))
    }

    attackRoll(event: AttackRollEvent) {
        if (event.attack.hasTag("light")) {
            event.attack.removeTag("light")
        }
    }
}

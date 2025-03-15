import { Character } from "../../main"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feat } from "../../sim/Feat"

export class Archery extends Feat {
    apply(character: Character): void {
        character.events.on("attack_roll", (event) => this.attackRoll(event))
    }

    attackRoll(event: AttackRollEvent) {
        if (event.attack.attack.weapon()?.hasTag("ranged")) {
            event.situationalBonus += 2
        }
    }
}

import { Character } from "../Character"
import { AttackResultEvent } from "../events/AttackResultEvent"
import { Feat } from "../Feat"

export class Topple extends Feat {
    apply(character: Character): void {
        character.events.on("attack_result", (data) => this.attackResult(data))
    }

    attackResult(data: AttackResultEvent): void {
        const weapon = data.attack.attack.weapon()
        const target = data.attack.target
        if (
            weapon &&
            weapon.mastery === "Topple" &&
            data.hit &&
            this.character.masteries.has("Topple") &&
            !target.save(this.character.dc(weapon.stat(this.character, data.attack.attack)))
        ) {
            target.knockProne()
        }
    }
}

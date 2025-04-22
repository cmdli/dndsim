import { Character } from "../Character"
import { AttackResultEvent } from "../events/AttackResultEvent"
import { Feature } from "../Feature"

export class Topple extends Feature {
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
            !target.save(
                this.character.dc(data.attack.attack.stat(this.character))
            )
        ) {
            target.knockProne()
        }
    }
}

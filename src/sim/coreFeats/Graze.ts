import { Character } from "../Character"
import { AttackResultEvent } from "../events/AttackResultEvent"
import { Feature } from "../Feat"

export class Graze extends Feature {
    apply(character: Character): void {
        character.events.on("attack_result", (data) => this.attackResult(data))
    }

    attackResult(data: AttackResultEvent): void {
        const weapon = data.attack.attack.weapon()
        if (
            !data.hit &&
            weapon &&
            weapon.mastery === "Graze" &&
            this.character?.masteries.has("Graze")
        ) {
            // Add damage directly because this is a miss
            data.attack.target.addDamage(
                "Graze",
                weapon.damageType,
                this.character?.mod(data.attack.attack.stat(this.character))
            )
        }
    }
}

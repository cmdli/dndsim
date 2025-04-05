import { Character } from "../Character"
import { AttackResultEvent } from "../events/AttackResultEvent"
import { Feat } from "../Feat"

export class Graze extends Feat {
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
            data.attack.target.addDamage(
                "Graze",
                weapon.damageType,
                this.character?.mod(weapon.mod(this.character))
            )
        }
    }
}

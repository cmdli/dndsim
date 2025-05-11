import { AttackResultEvent } from "../events/AttackResultEvent"
import { Feature } from "../Feature"

export class Graze extends Feature {
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

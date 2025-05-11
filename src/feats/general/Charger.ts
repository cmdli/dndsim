import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { BeginTurnEvent } from "../../sim/events/BeginTurnEvent"
import { Feature } from "../../sim/Feature"

export class Charger extends Feature {
    used: boolean = false

    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
    }

    beginTurn(event: BeginTurnEvent): void {
        this.used = false
    }

    attackResult(event: AttackResultEvent): void {
        // Lets assume you get this every turn optimistically
        if (!event.hit || this.used) {
            return
        }
        const weapon = event.attack?.attack.weapon()
        if (weapon && !event.attack?.attack.isRanged()) {
            event.addDamage({
                source: "Charger",
                dice: [8],
                type: weapon.damageType,
            })
            this.used = true
        }
    }
}

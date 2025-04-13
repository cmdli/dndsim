import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { BeginTurnEvent } from "../../sim/events/BeginTurnEvent"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Charger extends Feat {
    stat: Stat
    used: boolean = false

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        character.events.on("begin_turn", (event) => this.beginTurn(event))
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
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

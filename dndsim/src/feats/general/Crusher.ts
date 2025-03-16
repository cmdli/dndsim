import { Character } from "../../main"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { BeginTurnEvent } from "../../sim/events/BeginTurnEvent"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class Crusher extends Feat {
    stat: Stat
    enabled: boolean = false
    constructor(stat: "str" | "con") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        // We ignore the movement portion of the feat
        character.increaseStat(this.stat, 1)
        character.events.on("begin_turn", (event) => this.beginTurn(event))
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
    }

    beginTurn(event: BeginTurnEvent): void {
        this.enabled = false
    }

    attackRoll(event: AttackRollEvent): void {
        if (this.enabled) {
            event.adv = true
        }
    }

    attackResult(event: AttackResultEvent): void {
        if (!event.hit) {
            return
        }
        // TODO: Fix below
        // Technically this should work on any crit that
        // deals bludgeoning damage, but we just assume
        // it's only weapon damage for now
        if (
            event.crit &&
            event.attack?.attack.weapon()?.damageType === "bludgeoning"
        ) {
            this.enabled = true
        }
    }
}

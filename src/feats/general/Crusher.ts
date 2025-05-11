import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { BeginTurnEvent } from "../../sim/events/BeginTurnEvent"
import { Feature } from "../../sim/Feature"

export class Crusher extends Feature {
    enabled: boolean = false

    constructor(private stat: "str" | "con") {
        super()
    }

    apply(character: Character): void {
        // We ignore the movement portion of the feat
        character.increaseStat(this.stat, 1)
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
        if (
            event.crit &&
            event.damageRolls.some(
                (damageRoll) => damageRoll.type === "bludgeoning"
            )
        ) {
            this.enabled = true
        }
    }
}

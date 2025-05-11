import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { BeginTurnEvent } from "../../sim/events/BeginTurnEvent"
import { Feature } from "../../sim/Feature"
import { Stat } from "../../sim/types"

export class CombatProwess extends Feature {
    used: boolean = false

    constructor(private stat: Stat) {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
        character.increaseStat(this.stat, 1)
    }

    beginTurn(event: BeginTurnEvent): void {
        this.used = false
    }

    attackRoll(event: AttackRollEvent): void {
        if (!this.used && !event.hits()) {
            this.used = true
            event.autoHit = true
        }
    }
}

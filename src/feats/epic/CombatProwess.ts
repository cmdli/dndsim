import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { BeginTurnEvent } from "../../sim/events/BeginTurnEvent"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"

export class CombatProwess extends Feat {
    used: boolean = false

    constructor(private stat: Stat) {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
        character.increaseStat(this.stat, 1)
        character.events.on("begin_turn", (event) => this.beginTurn(event))
        character.events.on("attack_roll", (event) => this.attackRoll(event))
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

import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feature } from "../../sim/Feature"
import { Stat } from "../../sim/types"
import { rollDice } from "../../util/helpers"

// We only use Fate on attack rolls. In the future, it
// might be useful for causing the target to fail a save.
export class Fate extends Feature {
    used: boolean = false

    constructor(private stat: Stat) {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
        character.increaseStat(this.stat, 1)
    }

    shortRest(): void {
        this.used = false
    }

    attackRoll(event: AttackRollEvent): void {
        if (!this.used && !event.hits() && !event.isCritMiss()) {
            this.used = true
            event.situationalBonus += rollDice(2, 4)
        }
    }
}

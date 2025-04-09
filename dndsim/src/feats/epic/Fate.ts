import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"
import { rollDice } from "../../util/helpers"

// We only use Fate on attack rolls. In the future, it
// might be useful for causing the target to fail a save.
export class Fate extends Feat {
    used: boolean = false
    constructor(private stat: Stat) {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.stat, 1)
        character.increaseStat(this.stat, 1)
        character.events.on("short_rest", () => this.beginTurn())
        character.events.on("attack_roll", (event) => this.attackRoll(event))
    }

    beginTurn(): void {
        this.used = false
    }

    attackRoll(event: AttackRollEvent): void {
        if (!this.used && !event.hits() && !event.criticalMiss()) {
            this.used = true
            event.situationalBonus += rollDice(2, 4)
        }
    }
}

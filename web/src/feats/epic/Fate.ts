import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { BeginTurnEvent } from "../../sim/events/BeginTurnEvent"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"
import { rollDice } from "../../util/helpers"

// We only use Fate on attack rolls. In the future, it
// might be useful for causing the target to fail a save.
export class Fate extends Feat {
    stat: Stat
    used: boolean = false
    constructor(stat: Stat) {
        super()
        this.stat = stat
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
        if (event.roll() < event.attack.target.ac) {
            this.used = true
            event.situationalBonus += rollDice(2, 4)
        }
    }
}

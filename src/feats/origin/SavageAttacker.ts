import { Feature } from "../../sim/Feature"
import { Character } from "../../sim/Character"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { rollDice } from "../../util/helpers"
import { log } from "../../util/Log"
import { BeginTurnEvent } from "../../sim/events/BeginTurnEvent"

export class SavageAttacker extends Feature {
    used: boolean = false

    apply(character: Character): void {
        character.events.on("begin_turn", (data) => this.beginTurn(data))
        character.events.on("damage_roll", (data) => this.damageRoll(data))
    }

    beginTurn(data: BeginTurnEvent): void {
        this.used = false
    }

    damageRoll(args: DamageRollEvent): void {
        const weapon = args.attack?.attack.weapon()
        if (this.used || !weapon) {
            return
        }
        this.used = true
        const newRolls = args.damage.dice.map((die) => rollDice(1, die))
        if (
            newRolls.reduce((a, b) => a + b, 0) >
            args.damage.rolls.reduce((a, b) => a + b, 0)
        ) {
            args.damage.rolls = newRolls
            log.record(
                `Savage Attacker Improved (${weapon.name})`,
                newRolls.reduce((a, b) => a + b, 0)
            )
        }
    }
}

import { Feat } from "../../sim/Feat"
import { Character } from "../../sim/Character"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { rollDice } from "../../util/helpers"

export class SavageAttacker extends Feat {
    used: boolean = false

    apply(character: Character): void {
        character.events.on("damage_roll", (data) => this.damageRoll(data))
    }

    beginTurn(target: Character): void {
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
        }
    }
}

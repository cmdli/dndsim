import { Character } from "../../sim/Character"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feat } from "../../sim/Feat"
import { rollDice } from "../../util/helpers"

export class TavernBrawler extends Feat {
    apply(character: Character): void {
        character.events.on("damage_roll", (data) => this.damageRoll(data))
    }

    damageRoll(args: DamageRollEvent): void {
        for (let i = 0; i < args.damage.rolls.length; i++) {
            if (args.damage.rolls[i] === 1) {
                args.damage.rolls[i] = rollDice(1, args.damage.dice[i])
            }
        }
    }
}

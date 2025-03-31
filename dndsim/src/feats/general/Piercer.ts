import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feat } from "../../sim/Feat"
import { Stat } from "../../sim/types"
import { rollDice } from "../../util/helpers"

export class Piercer extends Feat {
    stat: Stat

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
        character.events.on("damage_roll", (event) => this.damageRoll(event))
    }

    attackResult(event: AttackResultEvent): void {
        if (!event.hit) {
            return
        }
        // TODO: Fix this below
        // This should work for all crits with piercing damage,
        // but we are going to ignore that edge case
        const weapon = event.attack?.attack.weapon()
        if (weapon && weapon.damageType === "piercing" && event.crit) {
            event.addDamage({ source: "Piercer", dice: [weapon.die] })
        }
    }

    damageRoll(event: DamageRollEvent): void {
        if (event.attack?.attack.weapon()?.damageType === "piercing") {
            // Reroll the lowest die
            let minRoll = 1000
            let minIndex = 0
            for (let i = 0; i < event.damage.rolls.length; i++) {
                if (event.damage.rolls[i] < minRoll) {
                    minRoll = event.damage.rolls[i]
                    minIndex = i
                }
            }
            event.damage.rolls[minIndex] = rollDice(
                1,
                event.damage.dice[minIndex]
            )
        }
    }
}

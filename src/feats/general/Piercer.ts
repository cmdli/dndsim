import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { DamageRollEvent } from "../../sim/events/DamageRollEvent"
import { Feature } from "../../sim/Feature"
import { rollDice } from "../../util/helpers"

export class Piercer extends Feature {
    used: boolean = false

    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
    }

    beginTurn(): void {
        this.used = false
    }

    attackResult(event: AttackResultEvent): void {
        if (!event.crit) {
            return
        }

        const piercingDice = event.damageRolls
            .filter(({ type }) => type === "piercing")
            .flatMap(({ dice }) => dice)
        if (piercingDice.length > 0) {
            const biggestDie = Math.max(...piercingDice)
            event.addDamage({
                source: "Piercer",
                dice: [biggestDie],
                type: "piercing",
            })
        }
    }

    // TODO: This assumes that every die for the attack is in this single damage roll event.
    // When attacks have multiple damage rolls, we could want to pick the best one.
    damageRoll(event: DamageRollEvent): void {
        if (this.used || event.damage.type !== "piercing") {
            return
        }

        // The expected increase could potentially be affected by things like Great Weapon Fighting
        let bestExpectedIncrease = 0
        let minIndex: number | null = null

        for (let i = 0; i < event.damage.rolls.length; i++) {
            const expectedIncrease =
                (event.damage.dice[i] + 1) / 2 - event.damage.rolls[i]
            if (expectedIncrease > bestExpectedIncrease) {
                bestExpectedIncrease = expectedIncrease
                minIndex = i
            }
        }

        if (minIndex !== null) {
            event.damage.rolls[minIndex] = rollDice(
                1,
                event.damage.dice[minIndex]
            )

            this.used = true
        }
    }
}

import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feat } from "../../sim/Feat"

export class ImprovedCritical extends Feat {
    minCrit: number

    constructor(minCrit: number) {
        super()
        this.minCrit = minCrit
    }

    apply(character: Character): void {
        character.events.on("attack_roll", (data: AttackRollEvent) => {
            if (!data.minCrit || data.minCrit >= this.minCrit) {
                data.minCrit = this.minCrit
            }
        })
    }
}

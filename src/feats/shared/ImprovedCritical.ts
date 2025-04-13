import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feat } from "../../sim/Feat"

export class ImprovedCritical extends Feat {
    constructor(private minCrit: number) {
        super()
    }

    apply(character: Character): void {
        character.events.on("attack_roll", (data: AttackRollEvent) => {
            if (data.minCrit >= this.minCrit) {
                data.minCrit = this.minCrit
            }
        })
    }
}

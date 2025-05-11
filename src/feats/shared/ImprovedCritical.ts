import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feature } from "../../sim/Feature"

export class ImprovedCritical extends Feature {
    constructor(private minCrit: number) {
        super()
    }

    attackRoll(event: AttackRollEvent): void {
        if (event.minCrit >= this.minCrit) {
            event.minCrit = this.minCrit
        }
    }
}

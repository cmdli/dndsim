import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feature } from "../../sim/Feature"

export class Lucky extends Feature {
    maxPoints: number = 0
    points: number = 0
    apply(character: Character): void {
        this.maxPoints = character.prof()
    }

    longRest(): void {
        this.points = this.maxPoints
    }

    attackRoll(event: AttackRollEvent): void {
        if (this.points > 0) {
            event.adv = true
            this.points--
        }
    }
}

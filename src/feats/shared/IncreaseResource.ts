import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feat"

export class IncreaseResource extends Feature {
    constructor(private resource: string, private value: number = 1) {
        super()
    }

    apply(character: Character): void {
        character.getResource(this.resource).addMax(this.value)
    }
}

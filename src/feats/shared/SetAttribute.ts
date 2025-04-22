import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"

export class SetAttribute extends Feature {
    constructor(private attribute: string, private value: number) {
        super()
    }

    apply(character: Character): void {
        const currentValue = character.getAttribute(this.attribute)
        if (currentValue < this.value) {
            character.setAttribute(this.attribute, this.value)
        }
    }
}

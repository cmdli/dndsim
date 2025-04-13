import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class SetAttribute extends Feat {
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

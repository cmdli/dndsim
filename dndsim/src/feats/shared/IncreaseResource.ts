import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class IncreaseResource extends Feat {
  constructor(private resource: string, private value: number = 1) {
    super()
  }

  apply(character: Character): void {
    character.getResource(this.resource).addMax(this.value)
  }
}


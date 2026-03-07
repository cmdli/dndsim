import { Character } from "../Character"
import { Feature } from "../Feature"

export class PseudoFeature extends Feature {
    constructor(private applyFunc: (character: Character) => void) {
        super()
    }

    apply(character: Character): void {
        this.applyFunc(character)
    }
}

import { Character } from "./Character"

export abstract class Feature {
    // Allow feats to expect the character to be set in their implementations
    // of apply
    declare character: Character

    internalApply(character: Character): void {
        this.character = character
        this.apply(character)
    }

    abstract apply(character: Character): void
}

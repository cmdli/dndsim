import { Character } from "./Character"

export abstract class Feat {
    character!: Character

    internalApply(character: Character): void {
        this.character = character
        this.apply(character)
    }

    abstract apply(character: Character): void
}

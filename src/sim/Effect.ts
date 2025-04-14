import { Character } from "./Character"

export type EffectDuration =
    | "permanent"
    | "round"
    | "until_short_rest"
    | "until_long_rest"

export abstract class Effect {
    character!: Character
    internalApply(character: Character): void {
        this.character = character
        this.apply(character)
    }

    abstract duration: EffectDuration
    abstract name: string
    abstract apply(character: Character): void
    abstract end(character: Character): void
}

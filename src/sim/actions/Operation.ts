import { Character } from "../Character"
import { Environment } from "../Environment"

export const TurnStages = [
    "turn_start",
    "before_action",
    "action",
    "after_action",
    "turn_end",
] as const

export type TurnStage = (typeof TurnStages)[number]

export interface Operation {
    readonly repeatable: boolean
    eligible(environment: Environment, character: Character): boolean
    do(environment: Environment, character: Character): void
}

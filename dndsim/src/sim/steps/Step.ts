import { Environment } from "../Environment"

export const StepStages = [
    "turn_start",
    "before_action",
    "action",
    "after_action",
    "turn_end",
] as const

export type StepStage = (typeof StepStages)[number]

export interface Step {
    stage(): StepStage
    eligible(environment: Environment): boolean
    do(environment: Environment): void
    repeatable(): boolean
}

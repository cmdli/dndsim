import { Environment } from "../Environment"
import { Step, StepStage } from "./Step"

export abstract class ActionStep implements Step {
    stage(): StepStage {
        return "action"
    }

    eligible(environment: Environment): boolean {
        return environment.character.actions > 0
    }

    do(environment: Environment): void {
        environment.character.actions--
        this.action(environment)
    }

    abstract action(environment: Environment): void
    abstract repeatable(): boolean
}

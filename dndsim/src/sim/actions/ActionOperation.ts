import { Character } from "../Character"
import { Environment } from "../Environment"
import { Operation, TurnStage } from "./Operation"

export abstract class ActionOperation implements Operation {
    stage: TurnStage = "action"

    eligible(environment: Environment, character: Character): boolean {
        return environment.character.actions.has()
    }

    do(environment: Environment, character: Character): void {
        environment.character.actions.use()
        this.action(environment, character)
    }

    abstract action(environment: Environment, character: Character): void
    abstract repeatable: boolean
}

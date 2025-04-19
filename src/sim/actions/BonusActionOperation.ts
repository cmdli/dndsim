import { Character } from "../Character"
import { Environment } from "../Environment"
import { Operation } from "./Operation"

export abstract class BonusActionOperation implements Operation {
    repeatable = true

    eligible(environment: Environment, character: Character): boolean {
        return character.bonus.has()
    }

    do(environment: Environment, character: Character): void {
        character.bonus.use()
    }

    abstract bonusAction(environment: Environment, character: Character): void
}

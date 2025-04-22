import { log } from "../../util/Log"
import { Character } from "../Character"
import { Environment } from "../Environment"
import { AfterActionEvent } from "../events/AfterActionEvent"
import { BeforeActionEvent } from "../events/BeforeActionEvent"
import { BeginTurnEvent } from "../events/BeginTurnEvent"
import { EndTurnEvent } from "../events/EndTurnEvent"
import { Operation, TurnStage } from "./Operation"

export class CustomTurn {
    priorityList: Record<TurnStage, Operation[]>

    constructor() {
        this.priorityList = {
            turn_start: [],
            before_action: [],
            action: [],
            after_action: [],
            turn_end: [],
        }
    }

    addOperation(stage: TurnStage, operation: Operation) {
        this.priorityList[stage].push(operation)
    }

    hasOperations(): boolean {
        for (const stage of Object.values(this.priorityList)) {
            if (stage.length > 0) {
                return true
            }
        }
        return false
    }

    doTurn(environment: Environment, character: Character) {
        const target = environment.target

        character.events.emit("begin_turn", new BeginTurnEvent({ target }))
        this.doStage(environment, character, this.priorityList["turn_start"])

        character.events.emit(
            "before_action",
            new BeforeActionEvent({ target })
        )
        this.doStage(environment, character, this.priorityList["before_action"])

        this.doStage(environment, character, this.priorityList["action"])

        character.events.emit("after_action", new AfterActionEvent({ target }))
        this.doStage(environment, character, this.priorityList["after_action"])

        character.events.emit("end_turn", new EndTurnEvent({ target }))
        this.doStage(environment, character, this.priorityList["turn_end"])
    }

    private doStage(
        environment: Environment,
        character: Character,
        steps: Operation[]
    ) {
        const stepList = steps.slice()
        let didStep = true
        while (didStep) {
            didStep = false
            for (let i = 0; i < stepList.length; i++) {
                const step = stepList[i]
                if (step.eligible(environment, character)) {
                    log.record(`Operation (${step.constructor.name})`, 1)
                    step.do(environment, character)
                    if (!step.repeatable) {
                        stepList.splice(i, 1)
                    }
                    didStep = true
                    break
                }
            }
        }
    }
}

import { Character } from "../Character"
import { Environment } from "../Environment"
import { AfterActionEvent } from "../events/AfterActionEvent"
import { BeforeActionEvent } from "../events/BeforeActionEvent"
import { BeginTurnEvent } from "../events/BeginTurnEvent"
import { EndTurnEvent } from "../events/EndTurnEvent"
import { Step, TurnStage } from "./Step"

export class CustomTurn {
    steps: Step[]

    constructor(steps: Step[]) {
        this.steps = steps
    }

    doTurn(environment: Environment, character: Character) {
        const target = environment.target
        const byStage: Partial<Record<TurnStage, Step[]>> = {}
        for (const step of this.steps) {
            const stage = step.stage()
            if (!byStage[stage]) {
                byStage[stage] = []
            }
            byStage[stage].push(step)
        }

        character.events.emit("begin_turn", new BeginTurnEvent({ target }))
        this.doStage(environment, character, byStage["turn_start"] || [])

        character.events.emit(
            "before_action",
            new BeforeActionEvent({ target })
        )
        this.doStage(environment, character, byStage["before_action"] || [])

        this.doStage(environment, character, byStage["action"] || [])

        character.events.emit("after_action", new AfterActionEvent({ target }))
        this.doStage(environment, character, byStage["after_action"] || [])

        character.events.emit("end_turn", new EndTurnEvent({ target }))
        this.doStage(environment, character, byStage["turn_end"] || [])
    }

    doStage(environment: Environment, character: Character, steps: Step[]) {
        let didStep = true
        while (didStep) {
            didStep = false
            for (let i = 0; i < steps.length; i++) {
                const step = steps[i]
                if (step.eligible(environment, character)) {
                    step.do(environment, character)
                    if (!step.repeatable()) {
                        steps.splice(i, 1)
                    }
                    didStep = true
                    break
                }
            }
        }
    }
}

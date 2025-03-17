import { Character } from "../Character"
import { Environment } from "../Environment"
import { Step, StepStage } from "./Step"

export class StepTurn {
    steps: Step[]

    constructor(steps: Step[]) {
        this.steps = steps
    }

    doTurn(environment: Environment) {
        const byStage: Partial<Record<StepStage, Step[]>> = {}
        for (const step of this.steps) {
            const stage = step.stage()
            if (!byStage[stage]) {
                byStage[stage] = []
            }
            byStage[stage].push(step)
        }
        this.doStage(environment, byStage["turn_start"] || [])
        this.doStage(environment, byStage["before_action"] || [])
        this.doStage(environment, byStage["action"] || [])
        this.doStage(environment, byStage["after_action"] || [])
        this.doStage(environment, byStage["turn_end"] || [])
    }

    doStage(environment: Environment, steps: Step[]) {
        let didStep = true
        while (didStep) {
            didStep = false
            for (let i = 0; i < steps.length; i++) {
                const step = steps[i]
                if (step.eligible(environment)) {
                    step.do(environment)
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

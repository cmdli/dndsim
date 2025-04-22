import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { Feature } from "../sim/Feature"
import { Class } from "../sim/types"

type ChoiceOption = {
    key: string
    name: string
    description: string
    featConfig: FeatConfig
}

export class Choice {
    name: string
    options: ChoiceOption[]
    constructor(args: { name: string; options: ChoiceOption[] }) {
        this.name = args.name
        this.options = args.options
    }

    apply(choices: Set<string>): Feature[] {
        for (const option of this.options) {
            if (choices.has(option.key)) {
                return option.featConfig.apply(choices)
            }
        }
        return []
    }
}

export class FeatConfig {
    feats: Feature[]
    choices: Choice[]
    constructor(feats: Feature[], choices?: Choice[]) {
        this.feats = feats
        this.choices = choices ?? []
    }

    apply(choices: Set<string>): Feature[] {
        const feats = []
        feats.push(...this.feats)
        for (const choice of this.choices) {
            feats.push(...choice.apply(choices))
        }
        return feats
    }
}

export class Schedule {
    schedule: Record<number, FeatConfig>
    constructor(schedule: Record<number, FeatConfig>) {
        this.schedule = schedule
    }

    apply(level: number, choices: Set<string>): Feature[] {
        const feats = []
        for (let i = 1; i <= level; i++) {
            const featConfig = this.schedule[i]
            if (featConfig) {
                feats.push(...featConfig.apply(choices))
            }
        }
        return feats
    }
}

export class ClassSchedule extends Schedule {
    class_: Class
    constructor(class_: Class, schedule: Record<number, FeatConfig>) {
        super(schedule)
        this.class_ = class_
    }

    apply(level: number, choices: Set<string>): Feature[] {
        const feats = []
        feats.push(...super.apply(level, choices))
        feats.push(new ClassLevel(this.class_, level))
        return feats
    }
}

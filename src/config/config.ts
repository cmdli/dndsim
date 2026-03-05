/**
 * - List of operations in priority order
 * - Button to add operation from list of available operations
 * - Each operation can have configuration choices
 *   - Select a weapon from available weapons
 *   - Select a spell from available spells
 *   - Select one of several static options
 * - Once every choice is configured, then the operation is added
 * - Each operation can be statically configured in code
 *
 *
 * ==== Choice Types ====
 *
 *
 * ClassLevel {
 *   feats: Feature[]
 *   choices: {
 *     mastery1: "string"
 *     mastery2: "string"
 *     fightingStyle: "string"
 *   }
 * }
 */

import { Feature } from "../sim/Feature"
import { Character } from "../sim/Character"

export interface Option {
    id: string
    choices(): Record<string, Choice>
    apply(character: Character, choices: Record<string, string>): void
}

export interface Choice {
    options(character: Character): Option[]
    apply(character: Character, optionId: string): void
}

export class StandardOption implements Option {
    id: string
    _choices: Record<string, Choice>
    feats: Feature[]

    constructor(args: {
        id: string
        choices?: Record<string, Choice>
        feats?: Feature[]
    }) {
        this.id = args.id
        this._choices = args.choices ?? {}
        this.feats = args.feats ?? []
    }

    choices(): Record<string, Choice> {
        return this._choices
    }

    apply(character: Character, choices: Record<string, string>): void {
        for (const choiceId of Object.keys(this._choices)) {
            if (choices[choiceId]) {
                this._choices[choiceId].apply(character, choices[choiceId])
            }
        }
        for (const feat of this.feats) {
            character.addFeature(feat)
        }
    }
}

export class StaticOption implements Option {
    id: string

    constructor(id: string) {
        this.id = id
    }

    choices(): Record<string, Choice> {
        return {}
    }

    apply(character: Character, choices: Record<string, string>): void {}
}

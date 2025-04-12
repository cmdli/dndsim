import { Character } from "../Character"
import { DamageRoll } from "../helpers/DamageRoll"
import { Target } from "../Target"
import { DamageType } from "../types"
import { SpellcastingSchool } from "./shared"

export type SpellArgs = {
    name: string
    level: number
    concentration?: boolean
    duration?: number
    school?: SpellcastingSchool
}

export class Spell<T = Target> {
    name: string
    level: number
    concentration: boolean
    duration: number
    school?: SpellcastingSchool
    declare character: Character

    constructor(args: SpellArgs) {
        this.name = args.name
        this.level = args.level
        this.concentration = args.concentration || false
        this.duration = args.duration || 0
        this.school = args.school
    }

    cast(character: Character, target?: T): void {
        this.character = character
    }

    end(character: Character): void { }
}

export class TargetedSpell extends Spell<Target> {
    cast(character: Character, target?: Target): void {
        super.cast(character, target)
        if (!target) {
            return
        }
        this.castTarget(character, target)
    }

    castTarget(character: Character, target: Target): void { }
}

export class ConcentrationSpell extends Spell<Target> {
    constructor(args: { name: string; level: number } & Partial<SpellArgs>) {
        super({ ...args, concentration: true })
    }

    cast(character: Character, target?: Target): void {
        super.cast(character, target)
        character.addEffect(this.name)
    }

    end(character: Character): void {
        super.end(character)
        character.removeEffect(this.name)
    }
}

export class BasicSaveSpell extends Spell {
    dice: number[]
    flatDmg: number
    type: DamageType

    constructor(
        args: {
            name: string
            level: number
            dice: number[]
            flatDmg?: number
            type: DamageType
        } & Partial<SpellArgs>
    ) {
        super(args)
        this.dice = args.dice
        this.flatDmg = args.flatDmg ?? 0
        this.type = args.type
    }

    cast(character: Character, target?: Target): void {
        if (!target) {
            return
        }
        super.cast(character, target)
        const saved = target.save(character.spells.dc())
        character.doDamage({
            target,
            damage: new DamageRoll({
                source: this.name,
                dice: this.dice,
                flatDmg: this.flatDmg,
                type: this.type,
            }),
            spell: this,
            multiplier: saved ? 0.5 : 1,
        })
    }
}

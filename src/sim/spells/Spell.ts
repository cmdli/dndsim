import { Character } from "../Character"
import { Effect, EffectDuration } from "../Effect"
import { DamageRoll } from "../helpers/DamageRoll"
import { Target } from "../Target"
import { DamageType } from "../types"
import { SpellcastingSchool } from "./shared"

export type CastingTime = "action" | "bonus_action" | "reaction"

export type SpellArgs = {
    name: string
    slot: number
    concentration?: boolean
    duration?: number
    school?: SpellcastingSchool
    castingTime: CastingTime
}

export class Spell {
    name: string
    slot: number
    concentration: boolean
    duration: number
    school?: SpellcastingSchool
    character!: Character
    castingTime: CastingTime
    constructor(args: SpellArgs) {
        this.name = args.name
        this.slot = args.slot
        this.concentration = args.concentration || false
        this.duration = args.duration || 0
        this.school = args.school
        this.castingTime = args.castingTime || "action"
    }

    cast(character: Character, target?: Target): void {
        this.character = character
    }

    end(character: Character): void {}
}

export class TargetedSpell extends Spell {
    cast(character: Character, target?: Target): void {
        super.cast(character, target)
        if (!target) {
            return
        }
        this.castTarget(character, target)
    }

    castTarget(character: Character, target: Target): void {}
}

export class ConcentrationSpellEffect extends Effect {
    name_: string
    duration: EffectDuration = "until_short_rest"

    constructor(name: string) {
        super()
        this.name_ = name
    }

    get name(): string {
        return this.name_
    }

    apply(character: Character): void {}
    end(character: Character): void {}
}

export class ConcentrationSpell extends Spell {
    constructor(
        args: {
            name: string
            slot: number
            castingTime: CastingTime
        } & Partial<SpellArgs>
    ) {
        super({ ...args, concentration: true })
    }

    cast(character: Character, target?: Target): void {
        super.cast(character, target)
        character.addEffect(this.effect())
    }

    end(character: Character): void {
        super.end(character)
        character.removeEffect(this.name)
    }

    // Override this to change the effect of the spell
    effect(): Effect {
        return new ConcentrationSpellEffect(this.name)
    }
}

export class BasicSaveSpell extends Spell {
    dice: number[]
    flatDmg: number
    type: DamageType

    constructor(
        args: {
            name: string
            slot: number
            dice: number[]
            flatDmg?: number
            type: DamageType
            castingTime: CastingTime
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

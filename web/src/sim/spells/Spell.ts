import { Character } from "../Character"
import { DamageRoll } from "../helpers/DamageRoll"
import { Target } from "../Target"
import { SpellcastingSchool } from "./shared"

export type SpellArgs = {
    name: string
    slot: number
    concentration?: boolean
    duration?: number
    school?: SpellcastingSchool
}

export class Spell {
    name: string
    slot: number
    concentration: boolean
    duration: number
    school?: SpellcastingSchool
    character?: Character

    constructor(args: SpellArgs) {
        this.name = args.name
        this.slot = args.slot
        this.concentration = args.concentration || false
        this.duration = args.duration || 0
        this.school = args.school
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

export class ConcentrationSpell extends Spell {
    constructor(args: { name: string; slot: number } & Partial<SpellArgs>) {
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

    constructor(
        args: {
            name: string
            slot: number
            dice: number[]
            flatDmg?: number
        } & Partial<SpellArgs>
    ) {
        super(args)
        this.dice = args.dice
        this.flatDmg = args.flatDmg || 0
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
            }),
            spell: this,
            multiplier: saved ? 0.5 : 1,
        })
    }
}

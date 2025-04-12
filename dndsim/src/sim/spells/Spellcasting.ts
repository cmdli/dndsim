import { Character } from "../Character"
import { Target } from "../Target"
import { Stat } from "../types"
import {
    Spellcaster,
    spellcasterLevel,
    highestSpellSlot,
    lowestSpellSlot,
    pactSpellSlots,
    spellSlots,
} from "./shared"
import { Spell } from "./Spell"

export class Spellcasting {
    character: Character
    stat: Stat = "int"
    spellcasterLevels: Array<[Spellcaster, number]>
    pactSpellcasterLevel: number
    concentration?: Spell
    spells: Array<Spell>
    slots: Array<number>
    pactSlots: Array<number>
    toHitBonus: number

    constructor(character: Character) {
        this.character = character
        this.spellcasterLevels = []
        this.pactSpellcasterLevel = 0
        this.spells = []
        this.slots = []
        this.pactSlots = []
        this.toHitBonus = 0
        this.character.events.on("short_rest", () => this.shortRest())
        this.character.events.on("long_rest", () => this.longRest())
    }

    setMod(mod: Stat): void {
        this.stat = mod
    }

    addSpellcasterLevel(spellcaster: Spellcaster, level: number): void {
        this.spellcasterLevels.push([spellcaster, level])
    }

    addPactSpellcasterLevel(level: number): void {
        this.pactSpellcasterLevel += level
    }

    addSlot(slot: number): void {
        // TODO: Check spell slot maximum here
        this.slots[slot] += 1
    }

    longRest(): void {
        this.slots = spellSlots(spellcasterLevel(this.spellcasterLevels))
        this.pactSlots = pactSpellSlots(this.pactSpellcasterLevel)
        this.shortRest()
    }

    shortRest(): void {
        this.setConcentration(undefined)
        for (const spell of this.spells) {
            spell.end(this.character)
        }
    }

    dc(): number {
        return 8 + this.character.mod(this.stat) + this.character.prof()
    }

    pactSlot(maxSlot: number = 9, minSlot: number = 1): number {
        if (this.pactSlots.length > 0) {
            const slot = this.pactSlots[0]
            if (slot <= maxSlot && slot >= minSlot) {
                return slot
            }
        }
        return 0
    }

    highestSlot(maxSlot: number = 9): number {
        const regularSlot = highestSpellSlot(this.slots, maxSlot)
        const pactSlot = this.pactSlot(maxSlot)
        return Math.max(regularSlot, pactSlot)
    }

    lowestSlot(minSlot: number = 1): number {
        const regularSlot = lowestSpellSlot(this.slots, minSlot)
        const pactSlot = this.pactSlot(undefined, minSlot)
        return Math.min(regularSlot, pactSlot)
    }

    cast(args: { spell: Spell; target?: Target; ignoreSlot?: boolean }): void {
        const { spell, target, ignoreSlot } = args
        if (spell.level > 0 && !ignoreSlot) {
            if (this.pactSlot() === spell.level) {
                this.pactSlots.pop()
            } else if (this.slots[spell.level] > 0) {
                this.slots[spell.level] -= 1
            } else {
                throw new Error(`Trying to use spell slot ${spell.level}`)
            }
        }
        if (spell.concentration) {
            this.setConcentration(spell)
        }
        spell.cast(this.character, target)
        if (spell.duration > 0 || spell.concentration) {
            this.spells.push(spell)
        }
    }

    endSpell(spell: Spell): void {
        this.spells = this.spells.filter((s) => s !== spell)
        spell.end(this.character)
    }

    setConcentration(spell?: Spell): void {
        if (this.concentration) {
            this.spells = this.spells.filter((s) => s !== this.concentration)
            this.concentration.end(this.character)
        }
        this.concentration = spell
    }

    concentratingOn(name: string): boolean {
        return this.concentration !== null && this.concentration?.name === name
    }

    isConcentrating(): boolean {
        return this.concentration !== null
    }

    cantripDice(): number {
        if (this.character.level >= 17) {
            return 4
        } else if (this.character.level >= 11) {
            return 3
        } else if (this.character.level >= 5) {
            return 2
        }
        return 1
    }

    toHit(): number {
        return (
            this.character.mod(this.stat) +
            this.character.prof() +
            this.toHitBonus
        )
    }
}

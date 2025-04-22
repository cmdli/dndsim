import { log } from "../../util/Log"
import { Character } from "../Character"
import { Target } from "../Target"
import { StatOrNone } from "../types"
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
    mod: StatOrNone = "none"
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

    setMod(mod: StatOrNone): void {
        this.mod = mod
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
        return 8 + this.character.mod(this.mod) + this.character.prof()
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
        if (!pactSlot) {
            return regularSlot
        }
        if (!regularSlot) {
            return pactSlot
        }
        return Math.max(regularSlot, pactSlot)
    }

    lowestSlot(minSlot: number = 1): number {
        const regularSlot = lowestSpellSlot(this.slots, minSlot)
        const pactSlot = this.pactSlot(undefined, minSlot)
        if (!pactSlot) {
            return regularSlot
        }
        if (!regularSlot) {
            return pactSlot
        }
        return Math.min(regularSlot, pactSlot)
    }

    hasSpellSlot(slot: number): boolean {
        return this.slots[slot] > 0 || this.pactSlots.includes(slot)
    }

    cast(args: { spell: Spell; target?: Target; ignoreSlot?: boolean }): void {
        const { spell, target, ignoreSlot } = args
        log.record(`Cast (${spell.name})`, 1)
        if (spell.slot > 0 && !ignoreSlot) {
            if (this.pactSlot() === spell.slot) {
                this.pactSlots.pop()
            } else if (this.slots[spell.slot] > 0) {
                this.slots[spell.slot] -= 1
            } else {
                throw new Error(`Trying to use spell slot ${spell.slot}`)
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
        return (
            this.concentration !== undefined &&
            this.concentration?.name === name
        )
    }

    isConcentrating(): boolean {
        return this.concentration !== undefined
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
            this.character.mod(this.mod) +
            this.character.prof() +
            this.toHitBonus
        )
    }
}

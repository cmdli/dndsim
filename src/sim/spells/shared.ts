export enum SpellcastingSchool {
    Abjuration = 1,
    Conjuration = 2,
    Divination = 3,
    Enchantment = 4,
    Evocation = 5,
    Illusion = 6,
    Necromancy = 7,
    Transmutation = 8,
}

export enum Spellcaster {
    Full = 1,
    Half = 2,
    Third = 3,
    None = 4,
}

export function spellcasterLevel(levels: Array<[Spellcaster, number]>): number {
    let total = 0
    for (const [type, level] of levels) {
        if (type === Spellcaster.Full) {
            total += level
        } else if (type === Spellcaster.Half) {
            total += Math.ceil(level / 2)
        } else if (type === Spellcaster.Third) {
            total += Math.ceil(level / 3)
        }
    }
    return total
}

const SPELL_SLOTS_ARR: Record<number, number[]> = {
    0: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    1: [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    2: [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
    3: [0, 4, 2, 0, 0, 0, 0, 0, 0, 0],
    4: [0, 4, 3, 0, 0, 0, 0, 0, 0, 0],
    5: [0, 4, 3, 2, 0, 0, 0, 0, 0, 0],
    6: [0, 4, 3, 3, 0, 0, 0, 0, 0, 0],
    7: [0, 4, 3, 3, 1, 0, 0, 0, 0, 0],
    8: [0, 4, 3, 3, 2, 0, 0, 0, 0, 0],
    9: [0, 4, 3, 3, 3, 1, 0, 0, 0, 0],
    10: [0, 4, 3, 3, 3, 2, 0, 0, 0, 0],
    11: [0, 4, 3, 3, 3, 2, 1, 0, 0, 0],
    12: [0, 4, 3, 3, 3, 2, 1, 0, 0, 0],
    13: [0, 4, 3, 3, 3, 2, 1, 1, 0, 0],
    14: [0, 4, 3, 3, 3, 2, 1, 1, 0, 0],
    15: [0, 4, 3, 3, 3, 2, 1, 1, 1, 0],
    16: [0, 4, 3, 3, 3, 2, 1, 1, 1, 0],
    17: [0, 4, 3, 3, 3, 2, 1, 1, 1, 1],
    18: [0, 4, 3, 3, 3, 3, 1, 1, 1, 1],
    19: [0, 4, 3, 3, 3, 3, 2, 1, 1, 1],
    20: [0, 4, 3, 3, 3, 3, 2, 2, 1, 1],
} as const

export function spellSlots(level: number): Array<number> {
    return SPELL_SLOTS_ARR[level].slice()
}

export function pactSpellSlots(level: number): Array<number> {
    if (level < 1) {
        return []
    }
    let slot = 1
    if (level >= 9) {
        slot = 5
    } else if (level >= 7) {
        slot = 4
    } else if (level >= 5) {
        slot = 3
    } else if (level >= 3) {
        slot = 2
    }
    let numSlots = 1
    if (level >= 17) {
        numSlots = 4
    } else if (level >= 11) {
        numSlots = 3
    } else if (level >= 5) {
        numSlots = 2
    }
    return Array(numSlots).fill(slot)
}

export function highestSpellSlot(
    slots: Array<number>,
    maxSlot: number = 9
): number {
    for (let i = maxSlot; i > 0; i--) {
        if (slots[i] > 0) {
            return i
        }
    }
    return 0
}

export function lowestSpellSlot(
    slots: Array<number>,
    minSlot: number = 1
): number {
    for (let i = minSlot; i <= 9; i++) {
        if (slots[i] > 0) {
            return i
        }
    }
    return 0
}

export function rollDice(numDice: number, die: number): number {
    let total = 0
    for (let i = 0; i < numDice; i++) {
        total += Math.floor(Math.random() * die) + 1
    }
    return total
}

export function diceRolls(dice: Array<number>): Array<number> {
    return dice.map((die) => rollDice(1, die))
}

const SPELL_SLOTS_ARR = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], // 0
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0], // 1
    [0, 3, 0, 0, 0, 0, 0, 0, 0, 0], // 2
    [0, 4, 2, 0, 0, 0, 0, 0, 0, 0], // 3
    [0, 4, 3, 0, 0, 0, 0, 0, 0, 0], // 4
    [0, 4, 3, 2, 0, 0, 0, 0, 0, 0], // 5
    [0, 4, 3, 3, 0, 0, 0, 0, 0, 0], // 6
    [0, 4, 3, 3, 1, 0, 0, 0, 0, 0], // 7
    [0, 4, 3, 3, 2, 0, 0, 0, 0, 0], // 8
    [0, 4, 3, 3, 3, 1, 0, 0, 0, 0], // 9
    [0, 4, 3, 3, 3, 2, 0, 0, 0, 0], // 10
    [0, 4, 3, 3, 3, 2, 1, 0, 0, 0], // 11
    [0, 4, 3, 3, 3, 2, 1, 0, 0, 0], // 12
    [0, 4, 3, 3, 3, 2, 1, 1, 0, 0], // 13
    [0, 4, 3, 3, 3, 2, 1, 1, 0, 0], // 14
    [0, 4, 3, 3, 3, 2, 1, 1, 1, 0], // 15
    [0, 4, 3, 3, 3, 2, 1, 1, 1, 0], // 16
    [0, 4, 3, 3, 3, 2, 1, 1, 1, 1], // 17
    [0, 4, 3, 3, 3, 3, 1, 1, 1, 1], // 18
    [0, 4, 3, 3, 3, 3, 2, 1, 1, 1], // 19
    [0, 4, 3, 3, 3, 3, 2, 2, 1, 1], // 20
]

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
    return Math.max(...slots.filter((slot) => slot <= maxSlot))
}

export function lowestSpellSlot(
    slots: Array<number>,
    minSlot: number = 1
): number {
    return Math.min(...slots.filter((slot) => slot >= minSlot))
}

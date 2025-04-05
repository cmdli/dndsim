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

export function profBonus(level: number): number {
    return Math.floor((level - 1) / 4) + 2
}

export function applyFeatSchedule<T>(args: {
    newFeats?: Array<T>
    schedule: Array<number>
    level: number
}): Array<T> {
    const { newFeats, schedule, level } = args
    if (!newFeats) {
        return []
    }
    const feats: T[] = []
    for (let i = 0; i < schedule.length; i++) {
        if (schedule[i] <= level && i < newFeats.length) {
            feats.push(newFeats[i])
        } else {
            break
        }
    }
    return feats
}

export function defaultMagicBonus(level: number): number {
    if (level >= 15) {
        return 3
    } else if (level >= 10) {
        return 2
    } else if (level >= 5) {
        return 1
    }
    return 0
}

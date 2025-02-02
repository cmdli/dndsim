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

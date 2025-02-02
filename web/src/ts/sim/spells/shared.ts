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

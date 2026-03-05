export type Stat = "Str" | "Dex" | "Con" | "Int" | "Wis" | "Cha"
// d20 checks can have no ability associated with them
export type StatOrNone = Stat | "none"

export const WEAPON_MASTERIES = [
    "Vex",
    "Topple",
    "Slow",
    "Nick",
    "Cleave",
    "Graze",
    "Sap",
    "Push",
] as const
export type WeaponMastery = (typeof WEAPON_MASTERIES)[number]

export type Class =
    | "Artificer"
    | "Barbarian"
    | "Bard"
    | "Cleric"
    | "Druid"
    | "Fighter"
    | "Monk"
    | "Paladin"
    | "Rogue"
    | "Ranger"
    | "Sorcerer"
    | "Warlock"
    | "Wizard"

export type DamageType =
    | "slashing"
    | "piercing"
    | "bludgeoning"
    | "fire"
    | "cold"
    | "acid"
    | "poison"
    | "lightning"
    | "thunder"
    | "radiant"
    | "necrotic"
    | "psychic"
    | "force"
    | "unknown"

export type Condition =
    | "blinded"
    | "charmed"
    | "deafened"
    | "exhaustion"
    | "frightened"
    | "grappled"
    | "incapacitated"
    | "invisible"
    | "paralyzed"
    | "petrified"
    | "poisoned"
    | "prone"
    | "restrained"
    | "stunned"
    | "semistunned"
    | "unconscious"

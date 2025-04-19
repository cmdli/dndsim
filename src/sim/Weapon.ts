import { DamageType, WeaponMastery } from "./types"

export const BaseWeaponDamageTag = "BaseWeaponDamage"

export const HeavyWeapon = "Heavy"
export const TwoHandedWeapon = "TwoHanded"
export const UnarmedWeapon = "Unarmed"
export const LightWeapon = "Light"
export const FinesseWeapon = "Finesse"
export const ThrownWeapon = "Thrown"
export const RangedWeapon = "Ranged"
export const LoadingWeapon = "Loading"
export const AmmunitionWeapon = "Ammunition"
export const VersatileWeapon = "Versatile"
export const ReachWeapon = "Reach"
export const SimpleWeapon = "Simple"
export const MartialWeapon = "Martial"

export type WeaponArgs = {
    name: string
    numDice?: number
    die: number
    damageType?: DamageType
    minCrit?: number
    mastery?: WeaponMastery
    magicBonus?: number
    attackBonus?: number
    dmgBonus?: number
    tags?: Array<string>
}

export class Weapon {
    readonly name: string
    readonly numDice: number
    readonly die: number
    readonly damageType: DamageType
    readonly minCrit: number
    readonly mastery?: WeaponMastery
    readonly magicBonus: number
    readonly attackBonus: number
    readonly dmgBonus: number
    readonly tags: Set<string>

    constructor(args: WeaponArgs, overrideArgs?: Partial<WeaponArgs>) {
        const merged = mergeArgs(args, overrideArgs)
        this.name = merged.name
        this.numDice = merged.numDice ?? 1
        this.die = merged.die
        this.damageType = merged.damageType ?? "unknown"
        this.minCrit = merged.minCrit ?? 20
        this.mastery = merged.mastery
        this.magicBonus = merged.magicBonus ?? 0
        this.attackBonus = this.magicBonus + (merged.attackBonus ?? 0)
        this.dmgBonus = this.magicBonus + (merged.dmgBonus ?? 0)
        this.tags = new Set(merged.tags)
    }

    rolls(crit: boolean): Array<number> {
        let numDice = this.numDice
        if (crit) {
            numDice *= 2
        }
        return Array(numDice).fill(this.die)
    }

    hasTag(tag: string): boolean {
        return this.tags.has(tag)
    }
}

function mergeArgs(
    args: WeaponArgs,
    overrideArgs?: Partial<WeaponArgs>
): WeaponArgs {
    return {
        ...args,
        ...overrideArgs,
        tags: [...(args.tags ?? []), ...(overrideArgs?.tags ?? [])],
    }
}

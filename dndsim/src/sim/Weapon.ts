import { DamageType, WeaponMastery } from "./types"

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

    constructor(args: WeaponArgs) {
        this.name = args.name
        this.numDice = args.numDice ?? 1
        this.die = args.die
        this.damageType = args.damageType ?? "unknown"
        this.minCrit = args.minCrit ?? 20
        this.mastery = args.mastery
        this.magicBonus = args.magicBonus ?? 0
        this.attackBonus = this.magicBonus + (args.attackBonus ?? 0)
        this.dmgBonus = this.magicBonus + (args.dmgBonus ?? 0)
        this.tags = new Set(args.tags)
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

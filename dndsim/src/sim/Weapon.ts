import { Attack } from "./Attack"
import { Character } from "./Character"
import { AttackResultEvent } from "./events/AttackResultEvent"
import { DamageType, Stat, WeaponMastery } from "./types"

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
    numDice: number
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
        this.numDice = args.numDice
        this.die = args.die
        this.damageType = args.damageType ?? "unknown"
        this.minCrit = args.minCrit ?? 20
        this.mastery = args.mastery
        this.magicBonus = args.magicBonus ?? 0
        this.attackBonus = this.magicBonus + (args.attackBonus ?? 0)
        this.dmgBonus = this.magicBonus + (args.dmgBonus ?? 0)
        this.tags = new Set(args.tags)
    }

    stat(character: Character, attack: Attack): Stat {
        const statsWithValues = attack.stats.map((stat) => [stat, character.stat(stat)] as const);
        return statsWithValues.reduce(([statA, valueA], [statB, valueB]) => {
            if (valueA > valueB) {
                return [statA, valueA]
            } else {
                return [statB, valueB]
            }
        })[0]
    }

    toHit(character: Character, attack: Attack): number {
        return (
            character.prof() +
            character.mod(this.stat(character, attack)) +
            this.attackBonus
        )
    }

    rolls(crit: boolean): Array<number> {
        let numDice = this.numDice
        if (crit) {
            numDice *= 2
        }
        return Array(numDice).fill(this.die)
    }

    attackResult(args: AttackResultEvent, character: Character): void {
        if (args.hit) {
            let damage = this.dmgBonus
            if (!args.attack.hasTag("light")) {
                damage += character.mod(this.stat(character, args.attack.attack))
            }
            args.addDamage({
                source: this.name,
                dice: Array(this.numDice).fill(this.die),
                flatDmg: damage,
                tags: new Set(["base_weapon_damage"]),
            })
        }
    }

    hasTag(tag: string): boolean {
        return this.tags.has(tag)
    }
}

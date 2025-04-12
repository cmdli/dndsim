import { Character } from "./Character"
import { AttackResultEvent } from "./events/AttackResultEvent"
import { Spell } from "./spells/Spell"
import { DamageType, Stat } from "./types"
import { FinesseWeapon, RangedWeapon, Weapon } from "./Weapon"

export abstract class Attack {
    tags: Set<string> = new Set()
    stats: Stat[] = []
    abstract damageType: DamageType

    abstract name(): string
    abstract toHit(character: Character): number
    abstract stat(character: Character): Stat
    abstract attackResult(args: AttackResultEvent, character: Character): void
    abstract minCrit(): number
    abstract isRanged(): boolean

    hasTag(tag: string): boolean {
        return this.tags.has(tag)
    }
    addTag(tag: string): void {
        this.tags.add(tag)
    }
    removeTag(tag: string): void {
        this.tags.delete(tag)
    }

    weapon(): Weapon | undefined {
        return undefined
    }
    spell(): Spell | undefined {
        return undefined
    }

    addStat(stat: Stat) {
        this.stats.push(stat)
    }
}

export class WeaponAttack extends Attack {
    readonly weapon_: Weapon
    readonly damageType: DamageType

    constructor(args: { weapon: Weapon; tags?: string[], damageType?: DamageType }) {
        super()
        this.weapon_ = args.weapon
        if (args.tags) {
            args.tags.forEach((tag) => this.addTag(tag))
        }
        if (this.weapon_.hasTag(FinesseWeapon)) {
            this.stats = ["str", "dex"]
        } else if (this.weapon_.hasTag(RangedWeapon)) {
            this.stats = ["dex"]
        } else {
            this.stats = ["str"]
        }

        this.damageType = args.damageType ?? this.weapon_.damageType
    }

    name(): string {
        return this.weapon_.name
    }

    stat(character: Character): Stat {
        const statsWithValues = this.stats.map((stat) => [stat, character.stat(stat)] as const);
        return statsWithValues.reduce(([statA, valueA], [statB, valueB]) => {
            if (valueA > valueB) {
                return [statA, valueA]
            } else {
                return [statB, valueB]
            }
        })[0]
    }

    toHit(character: Character): number {
        return (
            character.prof() +
            character.mod(this.stat(character)) +
            this.weapon_.attackBonus
        )
    }

    attackResult(args: AttackResultEvent, character: Character): void {
        if (!args.hit) {
            return
        }
        let damage = this.weapon_.dmgBonus
        if (!args.attack.hasTag("light")) {
            damage += character.mod(this.stat(character))
        }
        args.addDamage({
            source: this.weapon_.name,
            dice: Array(this.weapon_.numDice).fill(this.weapon_.die),
            flatDmg: damage,
            tags: new Set(["base_weapon_damage"]),
        })
    }

    minCrit(): number {
        return this.weapon_.minCrit
    }

    isRanged(): boolean {
        return this.weapon_.tags.has(RangedWeapon)
    }

    weapon(): Weapon {
        return this.weapon_
    }

    addStat(stat: Stat) {
        this.stats.push(stat)
    }
}

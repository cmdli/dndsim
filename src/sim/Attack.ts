import { Character } from "./Character"
import { AttackResultEvent } from "./events/AttackResultEvent"
import { Spell } from "./spells/Spell"
import { StatOrNone } from "./types"
import {
    BaseWeaponDamageTag,
    FinesseWeapon,
    RangedWeapon,
    Weapon,
} from "./Weapon"

export abstract class Attack {
    tags: Set<string> = new Set()
    stats: StatOrNone[] = []

    abstract name(): string
    abstract toHit(character: Character): number
    abstract stat(character: Character): StatOrNone
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

    addStat(stat: StatOrNone) {
        this.stats.push(stat)
    }
}

export class WeaponAttack extends Attack {
    private readonly weapon_: Weapon
    private readonly onResult?: (event: AttackResultEvent) => void

    constructor(args: {
        weapon: Weapon
        tags?: string[]
        onResult?: (event: AttackResultEvent) => void
    }) {
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
        this.onResult = args.onResult
    }

    name(): string {
        return this.weapon_.name
    }

    stat(character: Character): StatOrNone {
        return this.stats.reduce((best, stat) =>
            character.stat(best) > character.stat(stat) ? best : stat
        )
    }

    toHit(character: Character): number {
        return (
            character.prof() +
            character.mod(this.stat(character)) +
            this.weapon_.attackBonus
        )
    }

    attackResult(args: AttackResultEvent, character: Character): void {
        if (args.hit) {
            let damage = this.weapon_.dmgBonus
            if (!args.attack.hasTag("light")) {
                damage += character.mod(this.stat(character))
            }
            args.addDamage({
                source: this.weapon_.name,
                dice: Array(this.weapon_.numDice).fill(this.weapon_.die),
                flatDmg: damage,
                tags: [BaseWeaponDamageTag],
                type: this.weapon_.damageType,
            })
        }
        this.onResult?.(args)
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

    addStat(stat: StatOrNone) {
        this.stats.push(stat)
    }
}

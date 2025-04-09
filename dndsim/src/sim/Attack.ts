import { Character } from "./Character"
import { AttackResultEvent } from "./events/AttackResultEvent"
import { Spell } from "./spells/Spell"
import { Stat } from "./types"
import { FinesseWeapon, RangedWeapon, Weapon } from "./Weapon"

export abstract class Attack {
    tags: Set<string> = new Set()
    stats: Stat[] = []

    abstract name(): string
    abstract toHit(character: Character): number
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

    constructor(args: { weapon: Weapon; tags?: string[] }) {
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
    }

    name(): string {
        return this.weapon_.name
    }

    toHit(character: Character): number {
        return this.weapon_.toHit(character, this)
    }

    attackResult(args: AttackResultEvent, character: Character): void {
        this.weapon_.attackResult(args, character)
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

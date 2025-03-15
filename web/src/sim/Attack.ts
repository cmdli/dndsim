import { Character } from "./Character"
import { AttackResultEvent } from "./events/AttackResultEvent"
import { DamageRoll } from "./helpers/DamageRoll"
import { Spell } from "./spells/Spell"
import { Weapon } from "./Weapon"

export abstract class Attack {
    tags: Set<string> = new Set()

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
}

export class WeaponAttack extends Attack {
    readonly weapon_: Weapon

    constructor(args: { weapon: Weapon; tags?: string[] }) {
        super()
        this.weapon_ = args.weapon
        if (args.tags) {
            args.tags.forEach((tag) => this.addTag(tag))
        }
    }

    name(): string {
        return this.weapon_.name
    }

    toHit(character: Character): number {
        return this.weapon_.toHit(character)
    }

    attackResult(args: AttackResultEvent, character: Character): void {
        this.weapon_.attackResult(args, character)
    }

    minCrit(): number {
        return this.weapon_.minCrit
    }

    isRanged(): boolean {
        return this.weapon_.tags.has("ranged")
    }

    weapon(): Weapon {
        return this.weapon_
    }
}

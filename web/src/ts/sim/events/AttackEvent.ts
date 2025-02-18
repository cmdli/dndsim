import { Attack } from "../Attack"
import { Target } from "../Target"

export class AttackEvent {
    name: "attack" = "attack"
    target: Target
    attack: Attack
    tags: Set<string> = new Set()

    constructor(args: { target: Target; attack: Attack }) {
        this.target = args.target
        this.attack = args.attack
    }

    hasTag(tag: string): boolean {
        return this.tags.has(tag)
    }

    addTag(tag: string): void {
        this.tags.add(tag)
    }

    removeTag(tag: string): void {
        this.tags.delete(tag)
    }
}

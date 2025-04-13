import { DamageRoll } from "../helpers/DamageRoll"
import { Spell } from "../spells/Spell"
import { Target } from "../Target"
import { AttackEvent } from "./AttackEvent"

export class DamageRollEvent {
    name: "damage_roll" = "damage_roll"
    target: Target
    damage: DamageRoll
    attack?: AttackEvent // TODO: Convert to Attack object
    spell?: Spell // TODO: Merge with attack spell?

    constructor(args: {
        target: Target
        damage: DamageRoll
        attack?: AttackEvent
        spell?: Spell
    }) {
        this.target = args.target
        this.damage = args.damage
        this.attack = args.attack
        this.spell = args.spell
    }
}

import { DamageRoll } from "../helpers/DamageRoll"
import { AttackEvent } from "./AttackEvent"

export class AttackResultEvent {
    name: "attack_result" = "attack_result"
    attack: AttackEvent
    hit: boolean
    crit: boolean
    roll: number
    damageRolls: Array<DamageRoll>

    constructor(args: {
        attack: AttackEvent
        hit: boolean
        crit: boolean
        roll: number
    }) {
        this.attack = args.attack
        this.hit = args.hit
        this.crit = args.crit
        this.roll = args.roll
        this.damageRolls = []
    }

    addDamage(source: string, dice: Array<number>, flatDmg?: number): void {
        this.damageRolls.push(new DamageRoll({ source, dice, flatDmg }))
    }
}

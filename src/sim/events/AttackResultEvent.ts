import { DamageRoll } from "../helpers/DamageRoll"
import { DamageType } from "../types"
import { AttackEvent } from "./AttackEvent"

export class AttackResultEvent {
    name: "attack_result" = "attack_result"
    attack: AttackEvent
    hit: boolean
    crit: boolean
    roll: number
    damageRolls: Array<DamageRoll>
    dmgMultiplier: number = 1

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

    addDamage(args: {
        source: string
        dice?: Array<number>
        flatDmg?: number
        type: DamageType
        tags?: Array<string>
    }): void {
        const damageRoll = new DamageRoll(args)
        this.damageRolls.push(damageRoll)
    }
}

import { AttackEvent } from "./AttackEvent"
import { CharacterEvent } from "./CharacterEvent"

export class BeforeAttackEvent extends CharacterEvent {
    name: "before_attack" = "before_attack"

    constructor(public attackEvent: AttackEvent) {
        super()
    }
}

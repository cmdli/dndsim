import { Attack } from "../Attack"
import { Target } from "../Target"

export class AttackEvent {
    name: "attack" = "attack"
    target: Target
    attack: Attack

    constructor(args: { target: Target; attack: Attack }) {
        this.target = args.target
        this.attack = args.attack
    }
}

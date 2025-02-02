import { Target } from "../Target"
import { CharacterEvent } from "./CharacterEvent"

export class EnemyTurnEvent extends CharacterEvent {
    name: "enemy_turn" = "enemy_turn"
    target: Target

    constructor(args: { target: Target }) {
        super()
        this.target = args.target
    }
}

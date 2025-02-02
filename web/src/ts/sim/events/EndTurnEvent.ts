import { Target } from "../Target"
import { CharacterEvent } from "./CharacterEvent"

export class EndTurnEvent extends CharacterEvent {
    name: "end_turn" = "end_turn"
    target: Target

    constructor(args: { target: Target }) {
        super()
        this.target = args.target
    }
}

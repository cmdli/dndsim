import { Target } from "../Target"
import { CharacterEvent } from "./CharacterEvent"

export class BeginTurnEvent extends CharacterEvent {
    name: "begin_turn" = "begin_turn"
    target: Target

    constructor(args: { target: Target }) {
        super()
        this.target = args.target
    }
}

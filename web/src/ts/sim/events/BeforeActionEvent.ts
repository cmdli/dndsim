import { Target } from "../Target"
import { CharacterEvent } from "./CharacterEvent"

export class BeforeActionEvent extends CharacterEvent {
    name: "before_action" = "before_action"
    target: Target

    constructor(args: { target: Target }) {
        super()
        this.target = args.target
    }
}

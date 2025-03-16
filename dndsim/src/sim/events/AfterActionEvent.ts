import { Target } from "../Target"
import { CharacterEvent } from "./CharacterEvent"

export class AfterActionEvent extends CharacterEvent {
    name: "after_action" = "after_action"
    target: Target

    constructor(args: { target: Target }) {
        super()
        this.target = args.target
    }
}

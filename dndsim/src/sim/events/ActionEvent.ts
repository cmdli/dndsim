import { Target } from "../Target"
import { CharacterEvent } from "./CharacterEvent"

export class ActionEvent extends CharacterEvent {
    name: "action" = "action"
    target: Target

    constructor(args: { target: Target }) {
        super()
        this.target = args.target
    }
}

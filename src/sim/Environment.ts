import { Character } from "./Character"
import { Target } from "./Target"

export class Environment {
    character: Character
    target: Target

    constructor(args: { character: Character; target: Target }) {
        this.character = args.character
        this.target = args.target
    }
}

import { log } from "../../util/Log"
import { Character } from "../Character"

export class Resource {
    name: string
    count: number = 0
    max: number = 0

    resetOnShortRest: boolean = false

    constructor(args: {
        name: string
        character: Character
        initialMax: number
    }) {
        this.name = args.name
        this.count = args.initialMax
        this.max = args.initialMax
        args.character.events.on<"short_rest">("short_rest", () =>
            this.onShortRest()
        )
        args.character.events.on<"long_rest">("long_rest", () => this.reset())
    }

    addMax(amount: number): void {
        this.max += amount
    }

    use(reason?: string): boolean {
        if (this.count > 0) {
            log.record(`${this.name} (${reason})`, 1)
            this.count -= 1
            return true
        }
        return false
    }

    reset(): void {
        this.count = this.max
    }

    private onShortRest(): void {
        if (this.resetOnShortRest) {
            this.reset()
        }
    }
}

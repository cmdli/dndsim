import { log } from "../../util/Log"
import { Character } from "../Character"

export class Resource {
    name: string
    count: number = 0
    max: number = 0

    resetOnShortRest: boolean = false
    resetOnLongRest: boolean = false
    constructor(args: {
        name: string
        character: Character
        initialMax?: number
        initialCount?: number
        resetOnShortRest?: boolean
        resetOnLongRest?: boolean
    }) {
        this.name = args.name
        this.count = args.initialCount ?? args.initialMax ?? 0
        this.max = args.initialMax ?? 0
        args.character.events.on<"short_rest">("short_rest", () =>
            this.shortRest()
        )
        args.character.events.on<"long_rest">("long_rest", () =>
            this.longRest()
        )
        this.resetOnShortRest = args.resetOnShortRest ?? false
        this.resetOnLongRest = args.resetOnLongRest ?? false
    }

    addMax(amount: number): void {
        this.max += amount
    }

    add(amount: number): void {
        this.count = Math.min(this.max, this.count + amount)
    }

    use(reason?: string): boolean {
        if (this.count > 0) {
            log.record(`${this.name} (${reason})`, 1)
            this.count -= 1
            return true
        }
        return false
    }

    has(amount?: number): boolean {
        amount = amount ?? 1
        return this.count >= amount
    }

    reset(): void {
        this.count = this.max
    }

    private shortRest(): void {
        if (this.resetOnShortRest) {
            this.reset()
        }
    }

    private longRest(): void {
        if (this.resetOnLongRest) {
            this.reset()
        }
    }
}

import { log } from "../../util/Log"
import { Character } from "../Character"

export class Resource {
    name: string
    count: number = 0
    max: number = 0

    incrementOnShortRest: boolean = false
    resetOnShortRest: boolean = false
    resetOnLongRest: boolean = false

    constructor(args: {
        name: string
        character: Character
        initialMax?: number
        initialCount?: number
        incrementOnShortRest?: boolean
        resetOnShortRest?: boolean
        resetOnLongRest?: boolean
    }) {
        this.name = args.name
        this.count = args.initialCount ?? args.initialMax ?? 0
        this.max = args.initialMax ?? 0
        args.character.events.on("short_rest", () =>
            this.shortRest()
        )
        args.character.events.on("long_rest", () =>
            this.longRest()
        )
        this.resetOnShortRest = args.resetOnShortRest ?? false
        this.resetOnLongRest = args.resetOnLongRest ?? false
    }

    addMax(amount: number): void {
        this.max += amount
    }

    add(amount: number, overcount?: boolean): void {
        let newCount = this.count + amount
        if (!overcount) {
            newCount = Math.min(this.max, newCount)
        }
        this.count = newCount
    }

    use(amount: number): boolean
    use(reason?: string, amount?: number): boolean
    use(reasonOrAmount?: number | string, amountIfReason?: number): boolean {
        const reason = typeof reasonOrAmount === "string" ? reasonOrAmount : undefined
        const amount = typeof amountIfReason === "number"
            ? amountIfReason
            : typeof reasonOrAmount === "number"
                ? reasonOrAmount
                : 1

        if (this.count >= amount) {
            log.record(
                `Resource used: ${this.name}${reason ? ` (${reason})` : ""}`,
                amount
            )
            this.count -= amount
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
        if (this.incrementOnShortRest) {
            this.add(1)
        }
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

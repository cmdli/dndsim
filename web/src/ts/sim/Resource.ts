import {
    CharacterEvent,
    CharacterEventData,
    CharacterEventMapping,
    LongRestData,
    ShortRestData,
} from "./CharacterEvent"
import { EventLoop } from "./EventLoop"

export class Resource {
    name: string
    count: number = 0
    max: number = 0

    resetOnShortRest: boolean = false

    constructor(
        name: string,
        events: EventLoop<CharacterEvent, CharacterEventMapping>,
        initialMax: number
    ) {
        this.name = name
        this.count = initialMax
        this.max = initialMax
        events.addListener<"short_rest">("short_rest", () => this.onShortRest())
        events.addListener<"long_rest">("long_rest", () => this.reset())
    }

    addMax(amount: number): void {
        this.max += amount
    }

    use(reason?: string): boolean {
        if (this.count > 0) {
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

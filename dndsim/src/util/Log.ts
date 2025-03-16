class Log {
    record_: Map<string, number> = new Map()

    record(type: string, val: number): void {
        this.record_.set(type, (this.record_.get(type) ?? 0) + val)
    }

    printReport(): void {
        const keys = Array.from(this.record_.keys()).sort()
        for (const key of keys) {
            console.log(`${key} - ${this.record_.get(key)}`)
        }
    }
}

export const log = new Log()

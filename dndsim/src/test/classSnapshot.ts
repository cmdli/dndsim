import { testDPR, Character } from "../index"

const FLAT_UNCERTAINTY = 2.5
const PERCENT_UNCERTAINTY = 0.1

export function expectMatchesSnapshot(
    creator: (level: number) => Character,
    snapshot: number[][]
) {
    expect(snapshot.length).toBe(20)
    const results = testDPR({
        creator,
        startLevel: 1,
        endLevel: 20,
        numFights: 3,
        numRounds: 5,
        iterations: 5,
    })
    for (const [level, dpr] of snapshot) {
        const testDPR = results[level - 1][1]
        expect(testDPR).toBeGreaterThan(
            dpr * (1 - PERCENT_UNCERTAINTY) - FLAT_UNCERTAINTY
        )
        expect(testDPR).toBeLessThan(
            dpr * (1 + PERCENT_UNCERTAINTY) + FLAT_UNCERTAINTY
        )
    }
}

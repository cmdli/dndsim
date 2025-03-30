import { testDPR } from "../main"
import { Fighter } from "./Fighter"

const snapshot = [
    [1, 8.059333333333333],
    [2, 11.116666666666667],
    [3, 11.526666666666667],
    [4, 15.436],
    [5, 38.90133333333333],
    [6, 44.23866666666667],
    [7, 44.404666666666664],
    [8, 41.297333333333334],
    [9, 45.812666666666665],
    [10, 55.882666666666665],
    [11, 82.08866666666667],
    [12, 81.43133333333333],
    [13, 87.29066666666667],
    [14, 87.73666666666666],
    [15, 96.11533333333334],
    [16, 97.23333333333333],
    [17, 115.086],
    [18, 115.80466666666666],
    [19, 116.066],
    [20, 150.93466666666666],
]

describe("Fighter class", () => {
    it("should simulate a fighter", () => {
        const results = testDPR({
            creator: (level) => Fighter.createChampionFighter(level),
            startLevel: 1,
            endLevel: 20,
            numFights: 3,
            numRounds: 5,
            iterations: 5,
        })
        for (const [level, dpr] of snapshot) {
            const testDPR = results[level - 1][1]
            expect(testDPR).toBeGreaterThan(dpr * 0.9 - 2.5)
            expect(testDPR).toBeLessThan(dpr * 1.1 + 2.5)
        }
    })
})

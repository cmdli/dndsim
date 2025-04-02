import { expectMatchesSnapshot } from "../test/classSnapshot"
import { Monk } from "./Monk"

const snapshot = [
    [1, 9.004666666666667],
    [2, 9.360666666666667],
    [3, 10.044],
    [4, 18.102],
    [5, 29.002],
    [6, 30.054666666666666],
    [7, 30.624],
    [8, 38.76266666666667],
    [9, 40.15],
    [10, 46.824],
    [11, 52.614],
    [12, 59.318666666666665],
    [13, 61.33733333333333],
    [14, 63.13933333333333],
    [15, 65.36333333333333],
    [16, 72.77533333333334],
    [17, 77.476],
    [18, 77.716],
    [19, 78.04],
    [20, 94.69333333333333],
]

describe("Monk class", () => {
    it("should simulate a monk", () => {
        expectMatchesSnapshot(
            (level: number) => Monk.createOpenHandMonk(level),
            snapshot
        )
    })
})

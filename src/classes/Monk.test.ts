import { expectMatchesSnapshot } from "../test/classSnapshot"
import { Monk } from "./Monk"

const snapshot = [
    [1, 9.01],
    [2, 10.35],
    [3, 11.01],
    [4, 17.27],
    [5, 32.09],
    [6, 33.184],
    [7, 34.07],
    [8, 38.32],
    [9, 40.08],
    [10, 55.7],
    [11, 60.41],
    [12, 60.7],
    [13, 60.324],
    [14, 60.31],
    [15, 66.39],
    [16, 66.62],
    [17, 71.44],
    [18, 71.34],
    [19, 82.01],
    [20, 96.26],
]

describe("Monk class", () => {
    it("should simulate a monk", () => {
        expectMatchesSnapshot(
            (level: number) => Monk.createOpenHandMonk(level),
            snapshot
        )
    })
})

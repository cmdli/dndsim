import { testDPR } from "../main"
import { expectMatchesSnapshot } from "../test/classSnapshot"
import { Rogue } from "./Rogue"

const snapshot = [
    [1, 11.6],
    [2, 11.427333333333333],
    [3, 17.424666666666667],
    [4, 19.41],
    [5, 22.956],
    [6, 23.254],
    [7, 26.798],
    [8, 28.481333333333332],
    [9, 32.90866666666667],
    [10, 32.50533333333333],
    [11, 35.392],
    [12, 35.851333333333336],
    [13, 39.108],
    [14, 39.57066666666667],
    [15, 43.43933333333333],
    [16, 42.91866666666667],
    [17, 50.70333333333333],
    [18, 50.76533333333333],
    [19, 54.78066666666667],
    [20, 59.98466666666667],
]

describe("Rogue class", () => {
    it("should simulate a rogue", () => {
        expectMatchesSnapshot(
            (level: number) => Rogue.createAssassinRogue(level),
            snapshot
        )
    })
})

import { expectMatchesSnapshot } from "../test/classSnapshot"
import { Rogue } from "./Rogue"

const snapshot = [
    [1, 11.424],
    [2, 11.1],
    [3, 17.597333333333335],
    [4, 19.176666666666666],
    [5, 25.437333333333335],
    [6, 25.388666666666666],
    [7, 28.849333333333334],
    [8, 30.924666666666667],
    [9, 35.52],
    [10, 37.42133333333334],
    [11, 40.784],
    [12, 41.42133333333334],
    [13, 45.11333333333334],
    [14, 44.79066666666667],
    [15, 51.234],
    [16, 51.510666666666665],
    [17, 59.25333333333333],
    [18, 59.599333333333334],
    [19, 63.026],
    [20, 66.56866666666667],
]

describe("Rogue class", () => {
    it("should simulate a rogue", () => {
        expectMatchesSnapshot(
            (level: number) => Rogue.createAssassinRogue(level),
            snapshot
        )
    })
})

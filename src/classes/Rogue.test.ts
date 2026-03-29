import { expectMatchesSnapshot } from "../test/classSnapshot"
import { Rogue } from "./Rogue"

const assassinRogueSnapshot = [
    [1, 11.56],
    [2, 11.52],
    [3, 17.44],
    [4, 19.32],
    [5, 25.05],
    [6, 25.18],
    [7, 29.08],
    [8, 30.58],
    [9, 35.11],
    [10, 37.26],
    [11, 41.23],
    [12, 41.09],
    [13, 44.69],
    [14, 45.65533333333333],
    [15, 51.02],
    [16, 55.02],
    [17, 62.988],
    [18, 63.66],
    [19, 67.26],
    [20, 75.15],
]

const arcaneTricksterRogueSnapshot = [
    [1, 11.4],
    [2, 11.68],
    [3, 16.66],
    [4, 18.2],
    [5, 22.27],
    [6, 22.13],
    [7, 25.16],
    [8, 26.75],
    [9, 30.27],
    [10, 31.42],
    [11, 38.98],
    [12, 38.62],
    [13, 42.48],
    [14, 41.55],
    [15, 47.54],
    [16, 47.71],
    [17, 55.29],
    [18, 55.38],
    [19, 58.59],
    [20, 61.08],
]

const soulKnifeRogueSnapshot = [
    [1, 11.47],
    [2, 11.61],
    [3, 11.77],
    [4, 12.75],
    [5, 15.77],
    [6, 15.9],
    [7, 18.97],
    [8, 19.81],
    [9, 25.64],
    [10, 25.14],
    [11, 28.57],
    [12, 29.08],
    [13, 32.37],
    [14, 32.13],
    [15, 35.56],
    [16, 35.93],
    [17, 37.84],
    [18, 38.03],
    [19, 41.03],
    [20, 43.62],
]

describe("Rogue class", () => {
    it("matches the snapshots", () => {
        expectMatchesSnapshot(
            (level: number) => Rogue.createAssassinRogue(level),
            assassinRogueSnapshot
        )
        expectMatchesSnapshot(
            (level: number) => Rogue.createArcaneTricksterRogue(level),
            arcaneTricksterRogueSnapshot
        )
        expectMatchesSnapshot(
            (level: number) => Rogue.createSoulKnifeRogue(level),
            soulKnifeRogueSnapshot
        )
    })
})

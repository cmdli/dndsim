import { createChampionFighter } from "../classes/fighter"
import { testDPR } from "../sim/Simulation"

function createCharacter(level: number) {
    return createChampionFighter(level)
}

console.log(
    testDPR({
        creator: createCharacter,
        startLevel: 1,
        endLevel: 20,
        numFights: 5,
        numRounds: 3,
        iterations: 100,
    })
)

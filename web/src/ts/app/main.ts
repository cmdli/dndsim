import { createFighter } from "../classes/fighter"
import * as sim from "../sim/index"
import { testDPR } from "../sim/Simulation"

function createCharacter(level: number) {
    return createFighter(level)
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

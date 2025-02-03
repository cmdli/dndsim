import { createChampionFighter } from "../classes/fighter"
import { testDPR } from "../sim/Simulation"
import { log } from "../util/Log"

function createCharacter(level: number) {
    return createChampionFighter(level)
}

console.log(
    testDPR({
        creator: createCharacter,
        startLevel: 5,
        endLevel: 5,
        numFights: 3,
        numRounds: 5,
        iterations: 500,
    })
)

log.printReport()

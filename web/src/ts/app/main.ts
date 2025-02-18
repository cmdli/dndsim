import {
    createBattlemasterFighter,
    createChampionFighter,
} from "../classes/fighter"
import { testDPR } from "../sim/Simulation"
import { log } from "../util/Log"

console.log(
    testDPR({
        creator: createChampionFighter,
        startLevel: 1,
        endLevel: 20,
        numFights: 3,
        numRounds: 5,
        iterations: 500,
    })
)
console.log(
    testDPR({
        creator: createBattlemasterFighter,
        startLevel: 1,
        endLevel: 20,
        numFights: 3,
        numRounds: 5,
        iterations: 500,
    })
)

log.printReport()

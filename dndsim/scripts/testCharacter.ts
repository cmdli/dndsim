import * as dndsim from "../src/main"
import { log } from "../src/util/Log"

function testCharacter() {
    const results = dndsim.testDPR({
        creator: (level: number) =>
            dndsim.classes.Monk.createOpenHandMonk(level),
        startLevel: 1,
        endLevel: 20,
        numFights: 3,
        numRounds: 5,
        iterations: 100,
    })
    console.log(results)
    log.printReport()
}

testCharacter()

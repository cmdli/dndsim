import * as dndsim from "../src/index"
import { log } from "../src/util/Log"
import { program } from "commander"

type Args = {
    character: string
    startLevel: number
    endLevel: number
    numFights: number
    numRounds: number
    iterations: number
}

function parseArgs(): Args {
    program.option("--character <character>", "The character to test")
    program.option(
        "--start <startLevel>",
        "The starting level of the character",
        "1"
    )
    program.option(
        "--end <endLevel>",
        "The ending level of the character",
        "20"
    )
    program.option(
        "--fights <numFights>",
        "The number of fights to simulate",
        "3"
    )
    program.option(
        "--rounds <numRounds>",
        "The number of rounds to simulate",
        "5"
    )
    program.option(
        "--iterations <iterations>",
        "The number of iterations to simulate",
        "100"
    )
    program.parse(process.argv)
    const options = program.opts()
    return {
        character: options.character,
        startLevel: parseInt(options.start),
        endLevel: parseInt(options.end),
        numFights: parseInt(options.fights),
        numRounds: parseInt(options.rounds),
        iterations: parseInt(options.iterations),
    }
}

function getCharacterCreator(character: string) {
    switch (character) {
        case "monk":
            return (level: number) =>
                dndsim.classes.Monk.createOpenHandMonk(level)
        case "rogue":
            return (level: number) =>
                dndsim.classes.Rogue.createAssassinRogue(level)
        case "fighter":
            return (level: number) =>
                dndsim.classes.Fighter.createChampionFighter(level)
        case "barbarian":
            return (level: number) =>
                dndsim.classes.Barbarian.createZealotBarbarian(level)
        case "ranger":
            return (level: number) => dndsim.classes.Ranger.hunterRanger(level)
        default:
            throw new Error(`Unknown character: ${character}`)
    }
}

function testCharacter(args: Args) {
    const results = dndsim.testDPR({
        creator: getCharacterCreator(args.character),
        startLevel: args.startLevel,
        endLevel: args.endLevel,
        numFights: args.numFights,
        numRounds: args.numRounds,
        iterations: args.iterations,
    })
    console.log(results)
    log.printReport()
}

const args = parseArgs()
testCharacter(args)

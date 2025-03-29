import { log } from "../util/Log"
import { Character } from "./Character"
import { Target } from "./Target"

export class Simulation {
    character: Character
    target: Target
    numRounds: number
    numFights: number

    constructor(args: {
        character: Character
        target: Target
        numRounds: number
        numFights: number
    }) {
        this.character = args.character
        this.target = args.target
        this.numRounds = args.numRounds
        this.numFights = args.numFights
    }

    run() {
        this.character.longRest()
        this.target.longRest()
        for (let i = 0; i < this.numFights; i++) {
            for (let j = 0; j < this.numRounds; j++) {
                this.character.turn(this.target)
                this.character.enemyTurn(this.target)
                this.target.turn()
            }
            this.character.shortRest()
        }
        log.record("Damage (Total)", this.target.damage)
    }
}

export function testDPR(args: {
    creator: (level: number) => Character
    startLevel: number
    endLevel: number
    numFights: number
    numRounds: number
    iterations: number
    debug?: boolean
}) {
    const { creator, startLevel, endLevel, numFights, numRounds, iterations } =
        args
    const data = []
    for (let level = startLevel; level <= endLevel; level++) {
        let damage = 0
        for (let i = 0; i < iterations; i++) {
            const character = creator(level)
            const target = new Target({ level })
            const simulation = new Simulation({
                character,
                target,
                numRounds,
                numFights,
            })
            simulation.run()
            damage += target.damage
        }
        data.push([level, damage / (iterations * numFights * numRounds)])
    }
    return data
}

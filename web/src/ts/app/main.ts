import * as sim from "../sim/index"

const character = new sim.Character.Character()
character.turn(new sim.Target.Target())
character.shortRest()
console.log(character.bonus.count)

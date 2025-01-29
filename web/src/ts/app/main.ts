import * as sim from "../sim/index"

const character = new sim.Character.Character()
character.events.addListener("action", () => console.log("action"))
character.turn(new sim.Target.Target())
character.shortRest()
console.log(character.bonus.count)

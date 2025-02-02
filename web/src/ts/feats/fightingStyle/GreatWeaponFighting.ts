import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class GreatWeaponFighting extends Feat {
    apply(character: Character): void {
        character.events.on("damage_roll", (data) => {
            // TODO
        })
    }
}

import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feature } from "../../sim/Feature"

const CROSSBOWS = ["HandCrossbow", "LightCrossbow", "HeavyCrossbow"]

export class CrossbowExpert extends Feature {
    apply(character: Character): void {
        // We ignore firing in melee and the loading property
        character.increaseStat("dex", 1)
    }

    attackRoll(event: AttackRollEvent): void {
        const attack = event.attack?.attack
        const weapon = attack?.weapon()
        if (
            attack &&
            weapon &&
            CROSSBOWS.includes(weapon.name) &&
            attack.hasTag("light")
        ) {
            attack.removeTag("light")
        }
    }
}

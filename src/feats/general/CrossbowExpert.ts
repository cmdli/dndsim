import { Character } from "../../sim/Character"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feature } from "../../sim/Feat"

const CROSSBOWS = ["HandCrossbow", "LightCrossbow", "HeavyCrossbow"]

export class CrossbowExpert extends Feature {
    apply(character: Character): void {
        // We ignore firing in melee and the loading property
        character.increaseStat("dex", 1)
        character.events.on("attack_roll", (event) => this.attackRoll(event))
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

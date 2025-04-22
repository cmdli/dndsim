import { Character } from "../Character"
import { AttackResultEvent } from "../events/AttackResultEvent"
import { AttackRollEvent } from "../events/AttackRollEvent"
import { ShortRestEvent } from "../events/ShortRestEvent"
import { Feature } from "../Feat"

export class Vex extends Feature {
    vexing: boolean = false

    apply(character: Character): void {
        character.events.on("attack_roll", (data) => this.attackRoll(data))
    }

    shortRest(data: ShortRestEvent): void {
        this.vexing = false
    }

    attackRoll(data: AttackRollEvent): void {
        if (this.vexing) {
            data.adv = true
            this.vexing = false
        }
    }

    attackResult(data: AttackResultEvent): void {
        const weapon = data.attack.attack.weapon()
        if (
            data.hit &&
            weapon &&
            weapon.mastery === "Vex" &&
            this.character.masteries.has("Vex")
        ) {
            this.vexing = true
        }
    }
}

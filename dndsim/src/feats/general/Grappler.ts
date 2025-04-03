import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feat } from "../../sim/Feat"
import { UnarmedWeapon } from "../../sim/Weapon"

export class Grappler extends Feat {
    stat: "str" | "dex"

    constructor(stat: "str" | "dex") {
        super()
        this.stat = stat
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        character.events.on("attack_roll", (event) => this.attackRoll(event))
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
    }

    attackRoll(event: AttackRollEvent): void {
        if (event.attack?.target.grappled) {
            event.adv = true
        }
    }

    attackResult(event: AttackResultEvent): void {
        if (!event.hit) {
            return
        }
        const attack = event.attack
        const weapon = attack.attack.weapon()
        if (weapon && weapon.hasTag(UnarmedWeapon)) {
            this.character.grapple(attack.target)
        }
    }
}

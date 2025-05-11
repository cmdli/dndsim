import { AttackActionTag } from "../../sim/actions/AttackAction"
import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { AttackRollEvent } from "../../sim/events/AttackRollEvent"
import { Feature } from "../../sim/Feature"
import { UnarmedWeapon } from "../../sim/Weapon"

export class Grappler extends Feature {
    private used = false

    constructor(private stat: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
    }

    beginTurn() {
        this.used = false
    }

    attackRoll(event: AttackRollEvent): void {
        if (event.attack?.target.hasCondition("grappled")) {
            event.adv = true
        }
    }

    attackResult(event: AttackResultEvent): void {
        if (this.used || !event.hit) {
            return
        }
        const attack = event.attack
        const weapon = attack.attack.weapon()
        if (
            attack.attack.hasTag(AttackActionTag) &&
            weapon?.hasTag(UnarmedWeapon)
        ) {
            this.character.grapple(attack.target)
            this.used = true
        }
    }
}

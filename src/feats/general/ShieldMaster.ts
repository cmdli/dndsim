import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { Feat } from "../../sim/Feat"

export class ShieldMaster extends Feat {
    used: boolean = false

    apply(character: Character): void {
        // We ignore the Dex save benefits
        character.increaseStat("str", 1)
        character.events.on("begin_turn", () => this.beginTurn())
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
    }

    beginTurn(): void {
        this.used = false
    }

    attackResult(event: AttackResultEvent): void {
        // Assuming you have a shield here if you have this feat
        if (!event.hit) {
            return
        }
        const attack = event.attack.attack
        const target = event.attack.target
        if (attack.weapon() && !attack.isRanged()) {
            if (target.save(this.character.dc("str"))) {
                this.used = true
                target.knockProne()
            }
        }
    }
}

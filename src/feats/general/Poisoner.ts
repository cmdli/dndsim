import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { Feat } from "../../sim/Feat"

export class Poisoner extends Feat {
    uses: number = 0
    enabled: boolean = false

    constructor(private stat: "dex" | "int") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
        character.events.on("begin_turn", () => this.beginTurn())
    }

    longRest(): void {
        this.uses = this.character.prof()
    }

    beginTurn(): void {
        // TODO: Add ability to turn this on and off
        if (this.character.bonus.use()) {
            this.uses--
            this.enabled = true
        }
    }

    attackResult(event: AttackResultEvent): void {
        if (!event.hit) {
            return
        }
        if (this.enabled) {
            this.enabled = false
            if (!event.attack.target.save(this.character.dc(this.stat))) {
                event.addDamage({
                    source: "Poisoner",
                    dice: [8, 8],
                    type: "poison",
                })
                // Poisoned condition is untracked
            }
        }
    }
}

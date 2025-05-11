import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { Feature } from "../../sim/Feature"

export class Poisoner extends Feature {
    uses: number = 0
    enabled: boolean = false

    constructor(private stat: "dex" | "int") {
        super()
    }

    apply(character: Character): void {
        character.increaseStat(this.stat, 1)
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

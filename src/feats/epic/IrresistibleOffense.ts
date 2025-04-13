import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { Feat } from "../../sim/Feat"

export class IrresistibleOffense extends Feat {
    private mod: "str" | "dex"

    constructor(mod: "str" | "dex") {
        super()
        this.mod = mod
    }

    apply(character: Character): void {
        character.increaseStatMax(this.mod, 1)
        character.increaseStat(this.mod, 1)
        character.events.on("attack_result", (args) => this.attackResult(args))
    }

    attackResult(args: AttackResultEvent): void {
        const weapon = args.attack?.attack.weapon()
        if (weapon && args.hit && args.roll === 20) {
            args.addDamage({
                source: "IrresistibleOffense",
                flatDmg: this.character.stat(this.mod),
                type: weapon.damageType,
            })
        }
    }
}

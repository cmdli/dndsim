import { Character } from "../../sim/Character"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"
import { Feature } from "../../sim/Feature"

export class IrresistibleOffense extends Feature {
    constructor(private mod: "str" | "dex") {
        super()
    }

    apply(character: Character): void {
        character.increaseStatMax(this.mod, 1)
        character.increaseStat(this.mod, 1)
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

import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"
import { HeavyWeapon, Weapon } from "../../sim/Weapon"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"

export class GreatWeaponMaster extends Feat {
    private weapon: Weapon

    constructor(weapon: Weapon) {
        super()
        this.weapon = weapon
    }

    apply(character: Character): void {
        character.increaseStat("str", 1)
        character.events.on("attack_result", (data) => this.attackResult(data))
    }

    attackResult(data: AttackResultEvent): void {
        if (!data.hit) {
            return
        }
        if (data.attack.attack.weapon()?.hasTag(HeavyWeapon)) {
            data.addDamage({
                source: "GreatWeaponMaster",
                flatDmg: this.character?.prof(),
            })
        }
        if (data.crit && this.character?.bonus.use("GreatWeaponMaster")) {
            this.character?.weaponAttack({
                target: data.attack.target,
                weapon: this.weapon,
            })
        }
    }
}

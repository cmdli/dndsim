import { AttackActionTag } from "../../sim/actions/AttackAction"
import { Character } from "../../sim/Character"
import { Feature } from "../../sim/Feature"
import {
    HeavyWeapon,
    RangedWeapon,
    UnarmedWeapon,
    Weapon,
} from "../../sim/Weapon"
import { AttackResultEvent } from "../../sim/events/AttackResultEvent"

export class GreatWeaponMaster extends Feature {
    constructor(private weapon: Weapon) {
        super()
    }

    apply(character: Character): void {
        character.increaseStat("str", 1)
    }

    attackResult(data: AttackResultEvent): void {
        if (!data.hit) {
            return
        }

        const weapon = data.attack.attack.weapon()
        if (!weapon) {
            return
        }

        if (
            data.attack.attack.hasTag(AttackActionTag) &&
            weapon.hasTag(HeavyWeapon)
        ) {
            data.addDamage({
                source: "GreatWeaponMaster",
                flatDmg: this.character.prof(),
                type: weapon.damageType,
            })
        }
        if (
            data.crit &&
            !weapon.hasTag(RangedWeapon) &&
            !weapon.hasTag(UnarmedWeapon) &&
            this.character.bonus.use(1, "GreatWeaponMaster")
        ) {
            this.character.weaponAttack({
                target: data.attack.target,
                weapon: this.weapon,
            })
        }
    }
}

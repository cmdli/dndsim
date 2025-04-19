import {
    AmmunitionWeapon,
    HeavyWeapon,
    LoadingWeapon,
    RangedWeapon,
    TwoHandedWeapon,
    WeaponArgs,
} from "../../../sim/Weapon"
import { Weapon } from "../../../sim/Weapon"

export class HeavyCrossbow extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Heavy Crossbow",
                numDice: 1,
                die: 10,
                damageType: "piercing",
                mastery: "Push",
                tags: [
                    AmmunitionWeapon,
                    RangedWeapon,
                    LoadingWeapon,
                    HeavyWeapon,
                    TwoHandedWeapon,
                ],
            },
            args
        )
    }
}

import {
    AmmunitionWeapon,
    HeavyWeapon,
    LoadingWeapon,
    RangedWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Longbow extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Longbow",
                numDice: 1,
                die: 8,
                damageType: "piercing",
                mastery: "Slow",
                tags: [
                    AmmunitionWeapon,
                    RangedWeapon,
                    HeavyWeapon,
                    TwoHandedWeapon,
                    LoadingWeapon,
                ],
            },
            args
        )
    }
}

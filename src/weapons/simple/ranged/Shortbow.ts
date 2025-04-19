import {
    AmmunitionWeapon,
    RangedWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Shortbow extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Shortbow",
                numDice: 1,
                die: 6,
                damageType: "piercing",
                mastery: "Vex",
                tags: [TwoHandedWeapon, AmmunitionWeapon, RangedWeapon],
            },
            args
        )
    }
}

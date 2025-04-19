import {
    AmmunitionWeapon,
    LoadingWeapon,
    RangedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Pistol extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Pistol",
                numDice: 1,
                die: 10,
                damageType: "piercing",
                mastery: "Vex",
                tags: [AmmunitionWeapon, RangedWeapon, LoadingWeapon],
            },
            args
        )
    }
}

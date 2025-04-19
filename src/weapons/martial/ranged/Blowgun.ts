import {
    Weapon,
    WeaponArgs,
    AmmunitionWeapon,
    RangedWeapon,
    LoadingWeapon,
} from "../../../sim/Weapon"

export class Blowgun extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Blowgun",
                numDice: 0,
                die: 1,
                dmgBonus: 1 + (args?.dmgBonus ?? 0),
                damageType: "piercing",
                mastery: "Vex",
                tags: [AmmunitionWeapon, RangedWeapon, LoadingWeapon],
            },
            args
        )
    }
}

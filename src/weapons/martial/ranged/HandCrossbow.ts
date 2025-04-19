import {
    AmmunitionWeapon,
    LightWeapon,
    LoadingWeapon,
    RangedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class HandCrossbow extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Hand Crossbow",
                numDice: 1,
                die: 6,
                damageType: "piercing",
                mastery: "Vex",
                tags: [
                    AmmunitionWeapon,
                    LightWeapon,
                    RangedWeapon,
                    LoadingWeapon,
                ],
            },
            args
        )
    }
}

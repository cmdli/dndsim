import {
    AmmunitionWeapon,
    LoadingWeapon,
    RangedWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class LightCrossbow extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "LightCrossbow",
                numDice: 1,
                die: 6,
                damageType: "piercing",
                mastery: "Slow",
                tags: [
                    TwoHandedWeapon,
                    LoadingWeapon,
                    AmmunitionWeapon,
                    RangedWeapon,
                ],
            },
            args
        )
    }
}

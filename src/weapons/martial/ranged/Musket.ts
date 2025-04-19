import {
    AmmunitionWeapon,
    LoadingWeapon,
    RangedWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Musket extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Musket",
                numDice: 1,
                die: 12,
                damageType: "piercing",
                mastery: "Slow",
                tags: [
                    AmmunitionWeapon,
                    RangedWeapon,
                    LoadingWeapon,
                    TwoHandedWeapon,
                ],
            },
            args
        )
    }
}

import {
    AmmunitionWeapon,
    RangedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Sling extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Sling",
                numDice: 1,
                die: 4,
                damageType: "bludgeoning",
                mastery: "Slow",
                tags: [AmmunitionWeapon, RangedWeapon],
            },
            args
        )
    }
}

import {
    HeavyWeapon,
    ReachWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Pike extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Pike",
                numDice: 1,
                die: 10,
                damageType: "piercing",
                mastery: "Push",
                tags: [HeavyWeapon, ReachWeapon, TwoHandedWeapon],
            },
            args
        )
    }
}

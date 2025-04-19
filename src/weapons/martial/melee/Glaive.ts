import {
    HeavyWeapon,
    ReachWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Glaive extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Glaive",
                numDice: 1,
                die: 10,
                damageType: "slashing",
                mastery: "Graze",
                tags: [HeavyWeapon, TwoHandedWeapon, ReachWeapon],
            },
            args
        )
    }
}

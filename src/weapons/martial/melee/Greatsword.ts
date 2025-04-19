import {
    HeavyWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Greatsword extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Greatsword",
                numDice: 2,
                die: 6,
                damageType: "slashing",
                mastery: "Graze",
                tags: [HeavyWeapon, TwoHandedWeapon],
            },
            args
        )
    }
}

import {
    HeavyWeapon,
    ReachWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Halberd extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Halberd",
                numDice: 1,
                die: 10,
                damageType: "slashing",
                mastery: "Cleave",
                tags: [HeavyWeapon, ReachWeapon, TwoHandedWeapon],
            },
            args
        )
    }
}

import {
    HeavyWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Maul extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Maul",
                numDice: 2,
                die: 6,
                damageType: "bludgeoning",
                mastery: "Topple",
                tags: [HeavyWeapon, TwoHandedWeapon],
            },
            args
        )
    }
}

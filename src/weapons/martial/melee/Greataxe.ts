import {
    HeavyWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Greataxe extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Greataxe",
                numDice: 1,
                die: 12,
                damageType: "slashing",
                mastery: "Cleave",
                tags: [HeavyWeapon, TwoHandedWeapon],
            },
            args
        )
    }
}

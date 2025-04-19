import {
    FinesseWeapon,
    ReachWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Whip extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Whip",
                numDice: 1,
                die: 4,
                damageType: "slashing",
                mastery: "Slow",
                tags: [FinesseWeapon, ReachWeapon],
            },
            args
        )
    }
}

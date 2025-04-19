import {
    FinesseWeapon,
    LightWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Shortsword extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Shortsword",
                numDice: 1,
                die: 6,
                damageType: "slashing",
                mastery: "Vex",
                tags: [FinesseWeapon, LightWeapon],
            },
            args
        )
    }
}

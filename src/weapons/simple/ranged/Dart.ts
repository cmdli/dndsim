import {
    FinesseWeapon,
    ThrownWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Dart extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Dart",
                numDice: 1,
                die: 4,
                damageType: "piercing",
                mastery: "Vex",
                tags: [FinesseWeapon, ThrownWeapon],
            },
            args
        )
    }
}

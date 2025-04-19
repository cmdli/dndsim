import {
    ThrownWeapon,
    VersatileWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Trident extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Trident",
                numDice: 1,
                die: 8,
                damageType: "piercing",
                mastery: "Topple",
                tags: [ThrownWeapon, VersatileWeapon],
            },
            args
        )
    }
}

import {
    FinesseWeapon,
    LightWeapon,
    ThrownWeapon,
    Weapon,
    WeaponArgs,
} from "../../sim/Weapon"

export class Dagger extends Weapon {
    constructor(args?: WeaponArgs) {
        super({
            name: "Dagger",
            numDice: 1,
            die: 4,
            damageType: "piercing",
            mastery: "Nick",
            tags: [LightWeapon, FinesseWeapon, ThrownWeapon],
            ...args,
        })
    }
}

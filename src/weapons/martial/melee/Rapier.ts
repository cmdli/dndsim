import { FinesseWeapon, Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Rapier extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Rapier",
                numDice: 1,
                die: 8,
                damageType: "piercing",
                mastery: "Vex",
                tags: [FinesseWeapon],
            },
            args
        )
    }
}

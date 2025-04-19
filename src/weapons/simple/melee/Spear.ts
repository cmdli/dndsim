import { ThrownWeapon, Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Spear extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Spear",
                numDice: 1,
                die: 6,
                damageType: "piercing",
                mastery: "Sap",
                tags: [ThrownWeapon],
            },
            args
        )
    }
}

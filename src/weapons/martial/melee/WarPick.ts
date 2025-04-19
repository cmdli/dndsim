import { VersatileWeapon, Weapon, WeaponArgs } from "../../../sim/Weapon"

export class WarPick extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "WarPick",
                numDice: 1,
                die: 8,
                damageType: "piercing",
                mastery: "Sap",
                tags: [VersatileWeapon],
            },
            args
        )
    }
}

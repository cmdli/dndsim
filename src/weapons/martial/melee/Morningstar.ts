import { Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Morningstar extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Morningstar",
                numDice: 1,
                die: 8,
                damageType: "piercing",
                mastery: "Sap",
            },
            args
        )
    }
}

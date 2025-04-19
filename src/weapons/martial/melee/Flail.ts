import { Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Flail extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Flail",
                numDice: 1,
                die: 8,
                damageType: "bludgeoning",
                mastery: "Sap",
            },
            args
        )
    }
}

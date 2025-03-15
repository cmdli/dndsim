import { Weapon, WeaponArgs } from "../sim/Weapon"

export class Longsword extends Weapon {
    constructor(extraArgs?: Partial<WeaponArgs>) {
        super({
            name: "Longsword",
            numDice: 1,
            die: 8,
            damageType: "slashing",
            mastery: "Sap",
            ...extraArgs,
        })
    }
}

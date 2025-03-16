import { Weapon, WeaponArgs } from "../sim/Weapon"

export class Mace extends Weapon {
    constructor(args?: WeaponArgs) {
        super({
            name: "Mace",
            numDice: 1,
            die: 6,
            damageType: "bludgeoning",
            mastery: "Sap",
            ...args,
        })
    }
}

import { VersatileWeapon, Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Quarterstaff extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Quarterstaff",
                numDice: 1,
                die: 6,
                damageType: "bludgeoning",
                mastery: "Topple",
                tags: [VersatileWeapon],
            },
            args
        )
    }
}

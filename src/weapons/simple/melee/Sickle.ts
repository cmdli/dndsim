import { LightWeapon, Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Sickle extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Sickle",
                numDice: 1,
                die: 4,
                damageType: "slashing",
                mastery: "Nick",
                tags: [LightWeapon],
            },
            args
        )
    }
}

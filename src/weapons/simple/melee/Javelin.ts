import { ThrownWeapon, Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Javelin extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Javelin",
                numDice: 1,
                die: 6,
                damageType: "piercing",
                mastery: "Slow",
                tags: [ThrownWeapon],
            },
            args
        )
    }
}

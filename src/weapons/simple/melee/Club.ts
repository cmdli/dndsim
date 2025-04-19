import { LightWeapon, Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Club extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Club",
                numDice: 1,
                die: 4,
                damageType: "bludgeoning",
                mastery: "Slow",
                tags: [LightWeapon],
            },
            args
        )
    }
}

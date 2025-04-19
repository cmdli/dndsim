import { TwoHandedWeapon, Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Greatclub extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Greatclub",
                numDice: 1,
                die: 8,
                damageType: "bludgeoning",
                mastery: "Push",
                tags: [TwoHandedWeapon],
            },
            args
        )
    }
}

import { VersatileWeapon, Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Warhammer extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Warhammer",
                numDice: 1,
                die: 8,
                damageType: "bludgeoning",
                mastery: "Push",
                tags: [VersatileWeapon],
            },
            args
        )
    }
}

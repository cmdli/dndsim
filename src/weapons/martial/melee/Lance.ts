import {
    HeavyWeapon,
    ReachWeapon,
    TwoHandedWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Lance extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Lance",
                numDice: 1,
                die: 10,
                damageType: "piercing",
                mastery: "Topple",
                // TODO: Only two-handed while not mounted
                tags: [HeavyWeapon, ReachWeapon, TwoHandedWeapon],
            },
            args
        )
    }
}

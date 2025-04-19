import {
    FinesseWeapon,
    LightWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Scimitar extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Scimitar",
                numDice: 1,
                die: 6,
                damageType: "slashing",
                mastery: "Nick",
                tags: [FinesseWeapon, LightWeapon],
            },
            args
        )
    }
}

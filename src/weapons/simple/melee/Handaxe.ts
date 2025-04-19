import {
    LightWeapon,
    ThrownWeapon,
    Weapon,
    WeaponArgs,
} from "../../../sim/Weapon"

export class Handaxe extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Handaxe",
                numDice: 1,
                die: 6,
                damageType: "slashing",
                mastery: "Vex",
                tags: [LightWeapon, ThrownWeapon],
            },
            args
        )
    }
}

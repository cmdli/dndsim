import {
    UnarmedWeapon,
    Weapon,
    WeaponArgs,
} from "../../sim/Weapon"

export class UnarmedStrike extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super({
            name: "UnarmedStrike",
            numDice: 0,
            die: 1,
            dmgBonus: 1,
            damageType: "bludgeoning",
            tags: [UnarmedWeapon],
            ...args,
        })
    }
}


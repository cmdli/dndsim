import { VersatileWeapon, Weapon, WeaponArgs } from "../../../sim/Weapon"

export class Battleaxe extends Weapon {
    constructor(args?: Partial<WeaponArgs>) {
        super(
            {
                name: "Battleaxe",
                numDice: 1,
                die: 8,
                damageType: "slashing",
                mastery: "Topple",
                tags: [VersatileWeapon],
            },
            args
        )
    }
}

import { LightWeapon, ThrownWeapon, Weapon, WeaponArgs } from "../../sim/Weapon"

export class LightHammer extends Weapon {
    constructor(args?: WeaponArgs) {
        super({
            name: "LightHammer",
            numDice: 1,
            die: 4,
            damageType: "bludgeoning",
            mastery: "Nick",
            tags: [LightWeapon, ThrownWeapon],
            ...args,
        })
    }
}

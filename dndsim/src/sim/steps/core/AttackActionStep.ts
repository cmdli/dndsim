import { ActionStep } from "../ActionStep"
import { Character } from "../../Character"
import { Weapon } from "../../Weapon"
import { Environment } from "../../Environment"

// Represents a single weapon attack
export interface WeaponAttack {
    do(environment: Environment, character: Character): void
}

export const NumAttacksAttribute = "NumAttacks"

export class AttackActionStep extends ActionStep {
    weaponAttack: WeaponAttack
    constructor(weaponAttack: WeaponAttack) {
        super()
        this.weaponAttack = weaponAttack
    }

    action(environment: Environment, character: Character): void {
        const numAttacks = character.getAttribute(NumAttacksAttribute)
        for (let i = 0; i < numAttacks; i++) {
            this.weaponAttack.do(environment, character)
        }
    }

    repeatable(): boolean {
        return true
    }
}

export class DefaultAttackActionStep extends AttackActionStep {
    constructor(weapon: Weapon) {
        super(new RegularAttackStep(weapon))
    }
}

class RegularAttackStep implements WeaponAttack {
    weapon: Weapon
    constructor(weapon: Weapon) {
        this.weapon = weapon
    }

    do(environment: Environment, character: Character): void {
        character.weaponAttack({
            target: environment.target,
            weapon: this.weapon,
            tags: ["main_action"],
        })
    }
}

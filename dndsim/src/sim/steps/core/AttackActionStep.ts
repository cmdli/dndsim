import { ActionStep } from "../ActionStep"
import { Character } from "../../Character"
import { Weapon } from "../../Weapon"
import { Environment } from "../../Environment"

export const NumAttacksAttribute = "NumAttacks"

export class AttackActionStep extends ActionStep {
    weapon: Weapon
    constructor(weapon: Weapon) {
        super()
        this.weapon = weapon
    }

    action(environment: Environment): void {
        const numAttacks =
            environment.character.getAttribute(NumAttacksAttribute)
        for (let i = 0; i < numAttacks; i++) {
            environment.character.weaponAttack({
                target: environment.target,
                weapon: this.weapon,
                tags: ["main_action"],
            })
        }
    }

    repeatable(): boolean {
        return true
    }
}

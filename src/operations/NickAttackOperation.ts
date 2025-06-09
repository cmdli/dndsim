import { Character } from "../sim/Character"
import { Environment } from "../sim/Environment"
import { Weapon } from "../sim/Weapon"
import { AttackActionTag, MainActionTag } from "../sim/actions/AttackAction"
import { Operation } from "../sim/actions/Operation"

export class NickAttackOperation implements Operation {
    repeatable: boolean = false

    constructor(private weapon: Weapon) {
        if (weapon.mastery !== "Nick") {
            throw new Error(
                "NickAttackOperation must be used with a Nick weapon"
            )
        }
    }

    eligible(environment: Environment, character: Character): boolean {
        // Just assume that we used the attack action
        return true
    }

    do(environment: Environment, character: Character): void {
        character.weaponAttack({
            target: environment.target,
            weapon: this.weapon,
            tags: [AttackActionTag, MainActionTag],
        })
    }
}

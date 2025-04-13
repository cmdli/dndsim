import { Character } from "../Character"
import { Environment } from "../Environment"
import { Weapon } from "../Weapon"
import { AttackActionTag, MainActionTag } from "./AttackAction"
import { Operation } from "./Operation"

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

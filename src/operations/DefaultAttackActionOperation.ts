import { AttackActionOperation } from "../sim/actions/AttackAction"
import { MainActionTag } from "../sim/actions/AttackAction"
import { AttackActionTag } from "../sim/actions/AttackAction"
import { Weapon } from "../sim/Weapon"

export class DefaultAttackActionOperation extends AttackActionOperation {
    constructor(weapon: Weapon) {
        super((environment, character) => {
            character.weaponAttack({
                target: environment.target,
                weapon,
                tags: [AttackActionTag, MainActionTag],
            })
        })
    }
}

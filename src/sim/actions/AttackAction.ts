import { Character } from "../Character"
import { Target } from "../Target"
import { Weapon } from "../Weapon"
import { Environment } from "../Environment"
import { ActionOperation } from "./ActionOperation"

export const AttackActionTag = "AttackAction"
export const MainActionTag = "MainAction"
export const NumAttacksAttribute = "NumAttacks"

export function attackAction(args: {
    character: Character
    target: Target
    weapon: Weapon
}) {
    const { character, target, weapon } = args
    const numAttacks = args.character.getAttribute(NumAttacksAttribute)
    for (let i = 0; i < numAttacks; i++) {
        character.weaponAttack({
            target,
            weapon,
            tags: [MainActionTag, AttackActionTag],
        })
    }
}

export type WeaponAttack = (
    environment: Environment,
    character: Character
) => void

export class AttackActionOperation extends ActionOperation {
    repeatable: boolean = true

    weaponAttack: WeaponAttack
    constructor(weaponAttack: WeaponAttack) {
        super()
        this.weaponAttack = weaponAttack
    }

    action(environment: Environment, character: Character): void {
        const numAttacks = character.getAttribute(NumAttacksAttribute)
        for (let i = 0; i < numAttacks; i++) {
            this.weaponAttack(environment, character)
        }
    }
}

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

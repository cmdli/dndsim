import { Character } from "../Character"
import { Target } from "../Target"
import { Weapon } from "../Weapon"

export const NumAttacksAttribute = "NumAttacks"

export function attackAction(args: {
    character: Character
    target: Target
    weapon: Weapon
}) {
    const { character, target, weapon } = args
    const numAttacks = args.character.getAttribute(NumAttacksAttribute)
    for (let i = 0; i < numAttacks; i++) {
        character.weaponAttack({ target, weapon, tags: ["main_action"] })
    }
}

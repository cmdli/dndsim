import { Weapon } from "../sim/Weapon"
import { Character } from "../sim/Character"
import { SpellcastingSchool } from "../sim/spells/shared"
import { Spell } from "../sim/spells/Spell"
import { Target } from "../sim/Target"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"

const BoomingBladeTag = "booming_blade"

export class BoomingBlade extends Spell {
    constructor(private weapon: Weapon) {
        super({
            name: "BoomingBlade",
            slot: 0,
            school: SpellcastingSchool.Evocation,
            castingTime: "action",
        })
    }

    cast(character: Character, target?: Target) {
        if (!target) {
            throw new Error("Booming Blade must have a target")
        }
        const listener = (event: AttackResultEvent) => {
            if (event.hit && event.attack.attack.hasTag(BoomingBladeTag)) {
                const level = character.level
                let extraDice = 0
                if (level >= 17) {
                    extraDice = 3
                } else if (level >= 11) {
                    extraDice = 2
                } else if (level >= 5) {
                    extraDice = 1
                }
                if (extraDice > 0) {
                    event.addDamage({
                        source: "Booming Blade",
                        dice: Array(extraDice).fill(8),
                        type: "thunder",
                    })
                }
            }
        }
        character.weaponAttack({
            target,
            weapon: this.weapon,
            tags: [BoomingBladeTag],
            onResult: listener,
        })
    }
}

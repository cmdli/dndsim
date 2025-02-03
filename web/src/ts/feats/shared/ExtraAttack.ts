import { NumAttacksAttribute } from "../../sim/actions/AttackAction"
import { Character } from "../../sim/Character"
import { Feat } from "../../sim/Feat"

export class ExtraAttack extends Feat {
    numAttacks: number

    constructor(numAttacks: number) {
        super()
        this.numAttacks = numAttacks
    }

    apply(character: Character): void {
        const numAttacks = character.getAttribute(NumAttacksAttribute)
        if (numAttacks < this.numAttacks) {
            character.setAttribute(NumAttacksAttribute, this.numAttacks)
        }
    }
}

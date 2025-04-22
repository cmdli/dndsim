import { Character } from "../sim/Character"
import {
    ConcentrationSpell,
    ConcentrationSpellEffect,
} from "../sim/spells/Spell"
import { Effect } from "../sim/Effect"
import { Environment } from "../sim/Environment"
import { BonusActionOperation } from "../sim/actions/BonusActionOperation"
import { ActionOperation } from "../sim/actions/ActionOperation"
import { Attack } from "../sim/Attack"
import { StatOrNone } from "../sim/types"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"

class FeyBladeAttack extends Attack {
    constructor(private level: number, private caster: Character) {
        super()
    }

    name(): string {
        return "FeyBladeAttack"
    }

    toHit(character: Character): number {
        return this.caster.prof() + this.caster.mod(this.caster.spells.mod)
    }

    stat(character: Character): StatOrNone {
        return this.caster.spells.mod
    }

    attackResult(args: AttackResultEvent, character: Character): void {
        if (args.hit) {
            args.addDamage({
                source: "FeyBlade",
                type: "force",
                dice: [6, 6],
                flatDmg: 3 + this.level,
            })
        }
    }

    minCrit(): number {
        return 20
    }

    isRanged(): boolean {
        return false
    }
}

class FumingOperation extends BonusActionOperation {
    bonusAction(environment: Environment, character: Character): void {
        character.addTriggerEffect("attack_roll", (event) => {
            event.adv = true
            return "stop"
        })
    }
}

class MultiattackOperation extends ActionOperation {
    constructor(private level: number, private caster: Character) {
        super()
    }

    action(environment: Environment, character: Character): void {
        for (let i = 0; i < Math.floor(this.level / 2); i++) {
            character.attack({
                target: environment.target,
                attack: new FeyBladeAttack(this.level, this.caster),
            })
        }
    }
}

function feySummon(level: number, caster: Character): Character {
    const summon = new Character({
        stats: {
            str: 13,
            dex: 16,
            con: 14,
            int: 14,
            wis: 11,
            cha: 16,
        },
    })
    summon.customTurn.addOperation("before_action", new FumingOperation())
    summon.customTurn.addOperation(
        "action",
        new MultiattackOperation(level, caster)
    )

    return summon
}

class SummonFeyEffect extends ConcentrationSpellEffect {
    private minion?: Character
    constructor(private level: number, private caster: Character) {
        super("SummonFey")
    }

    apply(character: Character): void {
        this.minion = feySummon(this.level, this.caster)
        character.addMinion(this.minion)
    }

    end(character: Character): void {
        if (this.minion) {
            character.removeMinion(this.minion)
        }
    }
}

export class SummonFey extends ConcentrationSpell {
    constructor(slot: number) {
        super({
            name: "Summon Fey",
            slot,
            castingTime: "action",
        })
        if (slot < 3) {
            throw new Error("Summon Fey must be cast as a 3rd level spell")
        }
    }

    effect(): Effect {
        return new SummonFeyEffect(this.slot, this.character)
    }
}

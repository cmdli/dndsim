import { WeaponMastery } from "../sim/types"
import { Feat } from "../sim/Feat"
import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { applyFeatSchedule, defaultMagicBonus } from "../util/helpers"
import { Character } from "../sim/Character"
import { ExtraAttack } from "../feats/shared/ExtraAttack"
import { DamageRollEvent } from "../sim/events/DamageRollEvent"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { Archery } from "../feats/fightingStyle/Archery"
import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { DefaultAttackActionOperation } from "../sim/actions/AttackAction"
import { Longbow } from "../weapons/martial/ranged/Longbow"
import { CastSpellOperation } from "../sim/actions/CastSpellOperation"
import { SummonFey } from "../spells/SummonFey"
import { HuntersMark } from "../spells/HuntersMark"
import { Spellcaster } from "../sim/spells/shared"
import { SpellcastingFeat } from "../sim/spells/SpellcastingFeat"
import { BeginTurnEvent } from "../sim/events/BeginTurnEvent"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { ShortRestEvent } from "../sim/events/ShortRestEvent"

class PreciseHunter extends Feat {
    apply(character: Character): void {
        character.events.on("attack_roll", (event: AttackRollEvent) => {
            this.attackRoll(event)
        })
    }

    attackRoll(event: AttackRollEvent): void {
        if (this.character.hasEffect("HuntersMark")) {
            event.adv = true
        }
    }
}

class FoeSlayer extends Feat {
    apply(character: Character): void {
        character.events.on("damage_roll", (event: DamageRollEvent) => {
            this.damageRoll(event)
        })
    }

    damageRoll(event: DamageRollEvent): void {
        if (event.damage.source === "HuntersMark") {
            event.damage.replaceDice([10])
        }
    }
}

class ColossusSlayer extends Feat {
    used: boolean = false
    doneDamage: boolean = false

    apply(character: Character): void {
        character.events.on("short_rest", (event: ShortRestEvent) => {
            this.shortRest(event)
        })
        character.events.on("begin_turn", (event: BeginTurnEvent) => {
            this.beginTurn(event)
        })
        character.events.on("attack_result", (event: AttackResultEvent) => {
            this.attackResult(event)
        })
        character.events.on("damage_roll", (event: DamageRollEvent) => {
            this.damageRoll(event)
        })
    }

    shortRest(event: ShortRestEvent): void {
        this.used = false
        this.doneDamage = false
    }

    beginTurn(event: BeginTurnEvent): void {
        this.used = false
    }

    attackResult(event: AttackResultEvent): void {
        const weapon = event.attack.attack.weapon()
        if (event.hit && !this.used && weapon && this.doneDamage) {
            this.used = true
            event.addDamage({
                source: "ColossusSlayer",
                type: weapon.damageType,
                dice: [8],
            })
        }
    }

    damageRoll(event: DamageRollEvent): void {
        this.doneDamage = true
    }
}

export class Ranger {
    static baseFeats(args: {
        level: number
        asis: Array<Feat>
        masteries: WeaponMastery[]
        fightingStyle: Feat
    }): Feat[] {
        const { level, asis, masteries, fightingStyle } = args
        const feats: Feat[] = []
        if (level >= 1) {
            feats.push(new ClassLevel("Ranger", level))
            feats.push(new WeaponMasteries(masteries))
            feats.push(new SpellcastingFeat("wis", Spellcaster.Half, level))
        }
        // Level 2 (Deft Explorer) is irrelevant
        if (level >= 2) {
            feats.push(fightingStyle)
        }
        if (level >= 5) {
            feats.push(new ExtraAttack(2))
        }
        // Level 6 (Roving) is irrelevant
        // Level 9 (Expertise) is irrelevant
        // Level 10 (Tireless) is irrelevant
        // Level 13 (Relentless Hunter) is irrelevant
        // TODO: Level 14 (Nature's Veil)
        if (level >= 17) {
            feats.push(new PreciseHunter())
        }
        // Level 18 (Feral Senses) is irrelevant
        if (level >= 20) {
            feats.push(new FoeSlayer())
        }
        feats.push(
            ...applyFeatSchedule({
                newFeats: asis,
                schedule: [4, 8, 12, 16, 19],
                level,
            })
        )
        return feats
    }

    static hunterFeats(level: number): Feat[] {
        const feats: Feat[] = []
        if (level >= 3) {
            // Level 3 (Hunter's Lore) is irrelevant
            feats.push(new ColossusSlayer())
        }
        // Level 7 (Defensive Tactics) is irrelevant
        // Level 11 (Superior Hunter's Prey) is just bad
        // Level 15 (Superior Hunter's Defense) is irrelevant
        return feats
    }

    static hunterRanger(level: number): Character {
        const magicBonus = defaultMagicBonus(level)
        const character = new Character({
            stats: {
                str: 10,
                dex: 17,
                con: 10,
                int: 10,
                wis: 16,
                cha: 10,
            },
        })
        const feats: Feat[] = []
        feats.push(
            ...this.baseFeats({
                level,
                asis: [
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex", "wis"),
                    new AbilityScoreImprovement("wis"),
                    new AbilityScoreImprovement("wis"),
                    new IrresistibleOffense("dex"),
                ],
                masteries: ["Topple"],
                fightingStyle: new Archery(),
            })
        )
        feats.push(...this.hunterFeats(level))
        feats.forEach((feat) => character.addFeat(feat))

        character.customTurn.addOperation(
            "action",
            new CastSpellOperation((character) => {
                if (
                    character.spells.highestSlot() < 4 ||
                    character.spells.isConcentrating()
                ) {
                    return undefined
                }
                return new SummonFey(character.spells.lowestSlot(4))
            })
        )
        character.customTurn.addOperation(
            "action",
            new CastSpellOperation((character) => {
                if (character.spells.isConcentrating()) {
                    return undefined
                }
                return new HuntersMark(character.spells.lowestSlot())
            })
        )

        character.customTurn.addOperation(
            "action",
            new DefaultAttackActionOperation(new Longbow({ magicBonus }))
        )

        return character
    }
}

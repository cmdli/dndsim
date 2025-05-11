import { WeaponMastery } from "../sim/types"
import { Feature } from "../sim/Feature"
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

class PreciseHunter extends Feature {
    attackRoll(event: AttackRollEvent): void {
        if (this.character.hasEffect("HuntersMark")) {
            event.adv = true
        }
    }
}

class FoeSlayer extends Feature {
    damageRoll(event: DamageRollEvent): void {
        if (event.damage.source === "HuntersMark") {
            event.damage.replaceDice([10])
        }
    }
}

class ColossusSlayer extends Feature {
    used: boolean = false
    doneDamage: boolean = false

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
    static baseFeatures(args: {
        level: number
        asis: Array<Feature>
        masteries: WeaponMastery[]
        fightingStyle: Feature
    }): Feature[] {
        const { level, asis, masteries, fightingStyle } = args
        const features: Feature[] = []
        if (level >= 1) {
            features.push(new ClassLevel("Ranger", level))
            features.push(new WeaponMasteries(masteries))
            features.push(new SpellcastingFeat("wis", Spellcaster.Half, level))
        }
        // Level 2 (Deft Explorer) is irrelevant
        if (level >= 2) {
            features.push(fightingStyle)
        }
        if (level >= 5) {
            features.push(new ExtraAttack(2))
        }
        // Level 6 (Roving) is irrelevant
        // Level 9 (Expertise) is irrelevant
        // Level 10 (Tireless) is irrelevant
        // Level 13 (Relentless Hunter) is irrelevant
        // TODO: Level 14 (Nature's Veil)
        if (level >= 17) {
            features.push(new PreciseHunter())
        }
        // Level 18 (Feral Senses) is irrelevant
        if (level >= 20) {
            features.push(new FoeSlayer())
        }
        features.push(
            ...applyFeatSchedule({
                newFeats: asis,
                schedule: [4, 8, 12, 16, 19],
                level,
            })
        )
        return features
    }

    static hunterFeatures(level: number): Feature[] {
        const features: Feature[] = []
        if (level >= 3) {
            // Level 3 (Hunter's Lore) is irrelevant
            features.push(new ColossusSlayer())
        }
        // Level 7 (Defensive Tactics) is irrelevant
        // Level 11 (Superior Hunter's Prey) is just bad
        // Level 15 (Superior Hunter's Defense) is irrelevant
        return features
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
        const features: Feature[] = []
        features.push(
            ...this.baseFeatures({
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
        features.push(...this.hunterFeatures(level))
        features.forEach((feat) => character.addFeature(feat))

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

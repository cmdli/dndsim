import { WeaponMastery } from "../sim/types"
import { Feature } from "../sim/Feature"
import { AddClassLevel } from "../sim/coreFeats/ClassLevel"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { defaultMagicBonus, unreachable } from "../util/helpers"
import { Character } from "../sim/Character"
import { ExtraAttack } from "../feats/shared/ExtraAttack"
import { DamageRollEvent } from "../sim/events/DamageRollEvent"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { Archery } from "../feats/fightingStyle/Archery"
import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { DefaultAttackActionOperation } from "../operations/DefaultAttackActionOperation"
import { Longbow } from "../weapons/martial/ranged/Longbow"
import { CastSpellOperation } from "../operations/CastSpellOperation"
import { SummonFey } from "../spells/SummonFey"
import { HuntersMark } from "../spells/HuntersMark"
import { Spellcaster } from "../sim/spells/shared"
import { SpellcastingFeat } from "../sim/spells/SpellcastingFeat"
import { BeginTurnEvent } from "../sim/events/BeginTurnEvent"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { ShortRestEvent } from "../sim/events/ShortRestEvent"
import { FeatureGroup } from "../sim/helpers/FeatureGroup"

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

type RangerSubclass = "Hunter"

export class Ranger {
    static features(args: {
        level: number
        asis: Feature[]
        masteries: WeaponMastery[]
        fightingStyle: Feature
        subclass: RangerSubclass
    }): Feature[] {
        const { level, asis, masteries, fightingStyle, subclass } = args
        const features: Feature[] = []
        if (level >= 1) {
            features.push(Ranger.level1(level, masteries))
        }
        // Level 2 (Deft Explorer) is irrelevant
        if (level >= 2) {
            features.push(Ranger.level2(fightingStyle))
        }
        if (level >= 3) {
            features.push(Ranger.level3(subclass))
        }
        if (level >= 4) {
            features.push(Ranger.level4(asis[0]))
        }
        if (level >= 5) {
            features.push(Ranger.level5())
        }
        // Level 6 (Roving) is irrelevant
        if (level >= 8) {
            features.push(Ranger.level8(asis[1]))
        }
        // Level 9 (Expertise) is irrelevant
        // Level 10 (Tireless) is irrelevant
        if (level >= 12) {
            features.push(Ranger.level12(asis[2]))
        }
        // Level 13 (Relentless Hunter) is irrelevant
        // TODO: Level 14 (Nature's Veil)
        if (level >= 16) {
            features.push(Ranger.level16(asis[3]))
        }
        if (level >= 17) {
            features.push(Ranger.level17())
        }
        // Level 18 (Feral Senses) is irrelevant
        if (level >= 19) {
            features.push(Ranger.level19(asis[4]))
        }
        if (level >= 20) {
            features.push(Ranger.level20())
        }
        return features
    }

    static level1(level: number, masteries: WeaponMastery[]): Feature {
        return new FeatureGroup([
            new AddClassLevel("Ranger", level),
            new WeaponMasteries(masteries),
            new SpellcastingFeat("Wis", Spellcaster.Half, level),
        ])
    }

    static level2(fightingStyle: Feature): Feature {
        return new FeatureGroup([fightingStyle])
    }

    static level3(subclass: RangerSubclass): Feature {
        if (subclass === "Hunter") {
            // Level 3 (Hunter's Lore) is irrelevant
            return new FeatureGroup([new ColossusSlayer()])
        } else {
            unreachable(subclass)
        }
    }

    static level4(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level5(): Feature {
        return new FeatureGroup([new ExtraAttack(2)])
    }

    static level8(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level12(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level16(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level17(): Feature {
        return new FeatureGroup([new PreciseHunter()])
    }

    static level19(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level20(): Feature {
        return new FeatureGroup([new FoeSlayer()])
    }

    static hunterRanger(level: number): Character {
        const magicBonus = defaultMagicBonus(level)
        const character = new Character({
            stats: { Str: 10, Dex: 17, Con: 10, Int: 10, Wis: 16, Cha: 10 },
        })
        const features = Ranger.features({
            level,
            subclass: "Hunter",
            masteries: ["Topple"],
            fightingStyle: new Archery(),
            asis: [
                new AbilityScoreImprovement("Dex"),
                new AbilityScoreImprovement("Dex", "Wis"),
                new AbilityScoreImprovement("Wis"),
                new AbilityScoreImprovement("Wis"),
                new IrresistibleOffense("Dex"),
            ],
        })
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

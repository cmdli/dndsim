import { Environment } from "../sim/Environment"
import { Operation } from "../sim/actions/Operation"
import { Character } from "../sim/Character"
import { Feature } from "../sim/Feature"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { WeaponMastery } from "../sim/types"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { applyFeatSchedule, defaultMagicBonus } from "../util/helpers"
import { ExtraAttack } from "../feats/shared/ExtraAttack"
import { Resource } from "../sim/resources/Resource"
import { SavageAttacker } from "../feats/origin/SavageAttacker"
import { GreatWeaponMaster } from "../feats/general/GreatWeaponMaster"
import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { SetAttribute } from "../feats/shared/SetAttribute"
import { IncreaseResource } from "../feats/shared/IncreaseResource"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { Effect, EffectDuration } from "../sim/Effect"
import { DefaultAttackActionOperation } from "../sim/actions/AttackAction"
import { Greatsword } from "../weapons/martial/melee/Greatsword"

const RageResource = "rage"
const RageEffectName = "raging"
const RecklessTag = "reckless"

class RageEffect extends Effect {
    name = RageEffectName
    duration: EffectDuration = "until_short_rest"

    apply(character: Character): void {
        character.events.on("attack_result", this.attackResult)
    }

    end(character: Character): void {
        character.events.removeListener("attack_result", this.attackResult)
    }

    attackResult = (event: AttackResultEvent): void => {
        const weapon = event.attack?.attack.weapon()
        if (
            weapon &&
            event.hit &&
            event.attack.attack.stat(this.character) == "str"
        ) {
            event.addDamage({
                source: "Rage",
                flatDmg: this.character.getAttribute(RageBonusDamageAttribute),
                type: weapon.damageType,
            })
        }
    }
}

class RageOperation implements Operation {
    repeatable = false

    eligible(_environment: Environment, character: Character): boolean {
        // While it is techically possible to rage while raging, at this time
        // there is no benefit to doing so
        return (
            character.hasResource(RageResource) &&
            character.bonus.has() &&
            !character.hasEffect(RageEffectName)
        )
    }

    do(_environment: Environment, character: Character): void {
        character.useResource(RageResource)
        character.bonus.use()
        character.addEffect(new RageEffect())
    }
}

const RageBonusDamageAttribute = "rageBonusDamage"

class Rage extends Feature {
    apply(character: Character) {
        this.addResource()
        character.customTurn.addOperation("before_action", new RageOperation())
    }

    addResource() {
        this.character.resources.set(
            RageResource,
            new Resource({
                name: RageResource,
                character: this.character,
                initialMax: 2,
                incrementOnShortRest: true,
                resetOnLongRest: true,
            })
        )
    }
}

class RecklessAttack extends Feature {
    attackRoll(event: AttackRollEvent) {
        if (event.attack.attack.stat(this.character) == "str") {
            event.adv = true
            event.attack.addTag(RecklessTag)
        }
    }
}

class PrimalChampion extends Feature {
    apply(character: Character) {
        character.increaseStatAndMax("str", 4)
        character.increaseStatAndMax("con", 4)
    }
}

class Frenzy extends Feature {
    used = false

    beginTurn() {
        this.used = false
    }

    attackResult(event: AttackResultEvent) {
        const weapon = event.attack?.attack.weapon()
        if (
            weapon &&
            event.hit &&
            !this.used &&
            this.character.hasEffect(RageEffectName) &&
            event.attack?.hasTag(RecklessTag)
        ) {
            const dice = Array(
                this.character.getAttribute(RageBonusDamageAttribute)
            ).fill(6)
            event.addDamage({
                source: "Frenzy",
                dice,
                type: weapon.damageType,
            })
            this.used = true
        }
    }
}

class DivineFury extends Feature {
    used = false

    beginTurn() {
        this.used = false
    }

    attackResult(event: AttackResultEvent) {
        if (
            event.hit &&
            !this.used &&
            this.character.hasEffect(RageEffectName) &&
            event.attack?.attack.weapon()
        ) {
            event.addDamage({
                source: "DivineFury",
                dice: [6],
                flatDmg: Math.floor(
                    this.character.getClassLevel("Barbarian") / 2
                ),
                // This could also be necrotic instead
                type: "radiant",
            })
            this.used = true
        }
    }
}

export class Barbarian {
    static baseFeatures(args: {
        level: number
        asis: Array<Feature>
        masteries: WeaponMastery[]
    }): Feature[] {
        const { level, asis, masteries } = args
        const features: Feature[] = []
        if (level >= 1) {
            features.push(new ClassLevel("Barbarian", level))
            features.push(new WeaponMasteries(masteries))
            features.push(new SetAttribute(RageBonusDamageAttribute, 2))
            features.push(new Rage())
        }
        if (level >= 2) {
            features.push(new RecklessAttack())
        }
        if (level >= 3) {
            features.push(new IncreaseResource(RageResource))
        }
        if (level >= 5) {
            features.push(new ExtraAttack(2))
        }
        if (level >= 6) {
            features.push(new IncreaseResource(RageResource))
        }
        if (level >= 9) {
            features.push(new SetAttribute(RageBonusDamageAttribute, 3))
        }
        if (level >= 12) {
            features.push(new IncreaseResource(RageResource))
        }
        if (level >= 16) {
            features.push(new SetAttribute(RageBonusDamageAttribute, 4))
        }
        if (level >= 17) {
            features.push(new IncreaseResource(RageResource))
        }
        if (level >= 20) {
            features.push(new PrimalChampion())
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

    static berserkerFeatures(level: number): Feature[] {
        const features: Feature[] = []
        if (level >= 3) {
            features.push(new Frenzy())
        }
        // Level 6 (Mindless Rage) is ignored
        // Level 10 (Retaliation) is ignored
        // Level 14 (Intimidating Presence) is ignored
        return features
    }

    static zealotFeatures(level: number): Feature[] {
        const features: Feature[] = []
        if (level >= 3) {
            features.push(new DivineFury())
        }
        return features
    }

    static createBerserkerBarbarian(level: number): Character {
        const character = new Character({
            stats: { str: 17, dex: 10, con: 16, int: 10, wis: 10, cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })

        const features = [
            new SavageAttacker(),
            ...Barbarian.baseFeatures({
                level,
                asis: [
                    new GreatWeaponMaster(weapon),
                    new AbilityScoreImprovement("str"),
                    new AbilityScoreImprovement("con"),
                    new AbilityScoreImprovement("con"),
                    new IrresistibleOffense("str"),
                ],
                masteries: ["Topple", "Graze"],
            }),
            ...this.berserkerFeatures(level),
        ]
        features.forEach((feat) => character.addFeature(feat))

        character.customTurn.addOperation(
            "action",
            new DefaultAttackActionOperation(weapon)
        )
        return character
    }

    static createZealotBarbarian(level: number): Character {
        const character = new Character({
            stats: { str: 17, dex: 10, con: 16, int: 10, wis: 10, cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })

        const feats = [
            new SavageAttacker(),
            ...Barbarian.baseFeatures({
                level,
                asis: [
                    new GreatWeaponMaster(weapon),
                    new AbilityScoreImprovement("str"),
                    new AbilityScoreImprovement("con"),
                    new AbilityScoreImprovement("con"),
                    new IrresistibleOffense("str"),
                ],
                masteries: ["Topple", "Graze"],
            }),
            ...this.zealotFeatures(level),
        ]
        feats.forEach((feat) => character.addFeature(feat))

        character.customTurn.addOperation(
            "action",
            new DefaultAttackActionOperation(weapon)
        )
        return character
    }
}

import { Environment } from "../sim/Environment"
import { Operation } from "../sim/actions/Operation"
import { Character } from "../sim/Character"
import { Feature } from "../sim/Feature"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { WeaponMastery } from "../sim/types"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { AddClassLevel } from "../sim/coreFeats/ClassLevel"
import { defaultMagicBonus, unreachable } from "../util/helpers"
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
import { DefaultAttackActionOperation } from "../operations/DefaultAttackActionOperation"
import { Greatsword } from "../weapons/martial/melee/Greatsword"
import { FeatureGroup } from "../sim/helpers/FeatureGroup"

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
            event.attack.attack.stat(this.character) == "Str"
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
        if (event.attack.attack.stat(this.character) == "Str") {
            event.adv = true
            event.attack.addTag(RecklessTag)
        }
    }
}

class PrimalChampion extends Feature {
    apply(character: Character) {
        character.increaseStatAndMax("Str", 4)
        character.increaseStatAndMax("Con", 4)
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

type BarbarianSubclass = "Berserker" | "Zealot"

export class Barbarian {
    static operations = {
        RageOperation,
    }

    static features(args: {
        level: number
        asis: Feature[]
        masteries: WeaponMastery[]
        subclass: BarbarianSubclass
    }): Feature[] {
        const { level, asis, masteries, subclass } = args
        const features: Feature[] = []
        if (level >= 1) {
            features.push(Barbarian.level1(level, masteries))
        }
        if (level >= 2) {
            features.push(Barbarian.level2())
        }
        if (level >= 3) {
            features.push(Barbarian.level3(subclass))
        }
        if (level >= 4) {
            features.push(Barbarian.level4(asis[0]))
        }
        if (level >= 5) {
            features.push(Barbarian.level5())
        }
        if (level >= 6) {
            features.push(Barbarian.level6(subclass))
        }
        if (level >= 8) {
            features.push(Barbarian.level8(asis[1]))
        }
        if (level >= 9) {
            features.push(Barbarian.level9())
        }
        if (level >= 12) {
            features.push(Barbarian.level12(asis[2]))
        }
        if (level >= 16) {
            features.push(Barbarian.level16(asis[3]))
        }
        if (level >= 17) {
            features.push(Barbarian.level17())
        }
        if (level >= 19) {
            features.push(Barbarian.level19(asis[4]))
        }
        if (level >= 20) {
            features.push(Barbarian.level20())
        }
        return features
    }

    static level1(level: number, masteries: WeaponMastery[]): Feature {
        return new FeatureGroup([
            new AddClassLevel("Barbarian", level),
            new WeaponMasteries(masteries),
            new SetAttribute(RageBonusDamageAttribute, 2),
            new Rage(),
        ])
    }

    static level2(): Feature {
        return new FeatureGroup([new RecklessAttack()])
    }

    static level3(subclass: BarbarianSubclass): Feature {
        if (subclass === "Berserker") {
            return new FeatureGroup([
                new IncreaseResource(RageResource),
                new Frenzy(),
            ])
        } else if (subclass === "Zealot") {
            return new FeatureGroup([
                new IncreaseResource(RageResource),
                new DivineFury(),
            ])
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

    static level6(subclass: BarbarianSubclass): Feature {
        if (subclass === "Berserker") {
            // Level 6 (Mindless Rage) is ignored
            return new FeatureGroup([new IncreaseResource(RageResource)])
        } else if (subclass === "Zealot") {
            return new FeatureGroup([new IncreaseResource(RageResource)])
        } else {
            unreachable(subclass)
        }
    }

    static level8(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level9(): Feature {
        return new FeatureGroup([new SetAttribute(RageBonusDamageAttribute, 3)])
    }

    static level12(asi: Feature): Feature {
        return new FeatureGroup([new IncreaseResource(RageResource), asi])
    }

    static level16(asi: Feature): Feature {
        return new FeatureGroup([
            new SetAttribute(RageBonusDamageAttribute, 4),
            asi,
        ])
    }

    static level17(): Feature {
        return new FeatureGroup([new IncreaseResource(RageResource)])
    }

    static level19(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level20(): Feature {
        return new FeatureGroup([new PrimalChampion()])
    }

    static createBerserkerBarbarian(level: number): Character {
        const character = new Character({
            stats: { Str: 17, Dex: 10, Con: 16, Int: 10, Wis: 10, Cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })
        const features = [
            new SavageAttacker(),
            ...Barbarian.features({
                level,
                subclass: "Berserker",
                masteries: ["Topple", "Graze"],
                asis: [
                    new GreatWeaponMaster(weapon),
                    new AbilityScoreImprovement("Str"),
                    new AbilityScoreImprovement("Con"),
                    new AbilityScoreImprovement("Con"),
                    new IrresistibleOffense("Str"),
                ],
            }),
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
            stats: { Str: 17, Dex: 10, Con: 16, Int: 10, Wis: 10, Cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })
        const features = [
            new SavageAttacker(),
            ...Barbarian.features({
                level,
                subclass: "Zealot",
                masteries: ["Topple", "Graze"],
                asis: [
                    new GreatWeaponMaster(weapon),
                    new AbilityScoreImprovement("Str"),
                    new AbilityScoreImprovement("Con"),
                    new AbilityScoreImprovement("Con"),
                    new IrresistibleOffense("Str"),
                ],
            }),
        ]
        features.forEach((feat) => character.addFeature(feat))
        character.customTurn.addOperation(
            "action",
            new DefaultAttackActionOperation(weapon)
        )
        return character
    }
}

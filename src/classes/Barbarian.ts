import { Environment } from "../sim/Environment"
import { Operation } from "../sim/actions/Operation"
import { Character } from "../sim/Character"
import { Feat } from "../sim/Feat"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { WeaponMastery } from "../sim/types"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { applyFeatSchedule, defaultMagicBonus } from "../util/helpers"
import { ExtraAttack } from "../feats/shared/ExtraAttack"
import { Resource } from "../sim/resources/Resource"
import { Greatsword } from "../weapons"
import { SavageAttacker } from "../feats/origin/SavageAttacker"
import { GreatWeaponMaster } from "../feats/general/GreatWeaponMaster"
import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { SetAttribute } from "../feats/shared/SetAttribute"
import { IncreaseResource } from "../feats/shared/IncreaseResource"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"

const RageResource = "rage"
const RageEffect = "raging"
const RecklessTag = "reckless"

class RageOperation implements Operation {
    repeatable = false

    eligible(_environment: Environment, character: Character): boolean {
        // While it is techically possible to rage while raging, at this time
        // there is no benefit to doing so
        return character.hasResource(RageResource)
            && character.bonus.has()
            && !character.hasEffect(RageEffect)
    }

    do(_environment: Environment, character: Character): void {
        character.useResource(RageResource)
        character.bonus.use()
        character.addEffect(RageEffect)
    }
}

const RageBonusDamageAttribute = "rageBonusDamage"

class Rage extends Feat {
    apply(character: Character) {
        this.addResource()
        character.customTurn.addOperation("before_action", new RageOperation())
        character.events.on("attack_result", (event) => this.attackResult(event))
        character.events.on("short_rest", () => this.shortRest())
    }

    attackResult(event: AttackResultEvent) {
        if (event.hit && event.attack.attack.stat(this.character) == "str") {
            event.addDamage({
                source: "Rage",
                flatDmg: this.character.getAttribute(RageBonusDamageAttribute),
            })
        }
    }

    shortRest() {
        this.character.removeEffect(RageEffect)
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

class RecklessAttack extends Feat {
    apply(character: Character) {
        character.events.on("attack_roll", (event) => this.attackRoll(character, event))
    }

    attackRoll(character: Character, event: AttackRollEvent) {
        if (event.attack.attack.stat(character) == "str") {
            event.adv = true
            event.attack.addTag(RecklessTag)
        }
    }
}

class PrimalChampion extends Feat {
    apply(character: Character) {
        character.increaseStatAndMax("str", 4)
        character.increaseStatAndMax("con", 4)
    }
}

class Frenzy extends Feat {
    used = false

    apply(character: Character) {
        character.events.on("begin_turn", () => this.beginTurn())
        character.events.on("attack_result", (event) => this.attackResult(event))
    }

    beginTurn() {
        this.used = false
    }

    attackResult(event: AttackResultEvent) {
        if (event.hit && !this.used && this.character.hasEffect(RageEffect) && event.attack?.hasTag(RecklessTag)) {
            const dice = Array(this.character.getAttribute(RageBonusDamageAttribute)).fill(6)
            event.addDamage({
                source: "Frenzy",
                dice,
            })
            this.used = true
        }
    }
}

class DivineFury extends Feat {
    used = false

    apply(character: Character) {
        character.events.on("begin_turn", () => this.beginTurn())
        character.events.on("attack_result", (event) => this.attackResult(event))
    }

    beginTurn() {
        this.used = false
    }

    attackResult(event: AttackResultEvent) {
        if (event.hit && !this.used && this.character.hasEffect(RageEffect) && event.attack?.attack.weapon()) {
            event.addDamage({
                source: "DivineFury",
                dice: [6],
                flatDmg: Math.floor(this.character.getClassLevel("Barbarian") / 2),
                // This could also be necrotic instead
                type: 'radiant',

            })
            this.used = true
        }
    }
}

export class Barbarian {
    static baseFeats(args: {
        level: number
        asis: Array<Feat>
        masteries: WeaponMastery[]
    }): Feat[] {
        const { level, asis, masteries } = args
        const feats: Feat[] = []
        if (level >= 1) {
            feats.push(new ClassLevel("Barbarian", level))
            feats.push(new WeaponMasteries(masteries))
            feats.push(new SetAttribute(RageBonusDamageAttribute, 2))
            feats.push(new Rage())
        }
        if (level >= 2) {
            feats.push(new RecklessAttack())
        }
        if (level >= 3) {
            feats.push(new IncreaseResource(RageResource))
        }
        if (level >= 5) {
            feats.push(new ExtraAttack(2))
        }
        if (level >= 6) {
            feats.push(new IncreaseResource(RageResource))
        }
        if (level >= 9) {
            feats.push(new SetAttribute(RageBonusDamageAttribute, 3))
        }
        if (level >= 12) {
            feats.push(new IncreaseResource(RageResource))
        }
        if (level >= 16) {
            feats.push(new SetAttribute(RageBonusDamageAttribute, 4))
        }
        if (level >= 17) {
            feats.push(new IncreaseResource(RageResource))
        }
        if (level >= 20) {
            feats.push(new PrimalChampion())
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

    static berserkerFeats(level: number): Feat[] {
        const feats: Feat[] = []
        if (level >= 3) {
            feats.push(new Frenzy())
        }
        return feats
    }

    static zealotFeats(level: number): Feat[] {
        const feats: Feat[] = []
        if (level >= 3) {
            feats.push(new DivineFury())
        }
        return feats
    }

    static createBerserkerBarbarian(level: number): Character {
        const character = new Character({
            stats: { str: 17, dex: 10, con: 16, int: 10, wis: 10, cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })

        const feats = [
            new SavageAttacker(),
            ...Barbarian.baseFeats({
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
            ...this.berserkerFeats(level)
        ]
        feats.forEach((feat) => character.addFeat(feat))
        return character
    }

    static createZealotBarbarian(level: number): Character {
        const character = new Character({
            stats: { str: 17, dex: 10, con: 16, int: 10, wis: 10, cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })

        const feats = [
            new SavageAttacker(),
            ...Barbarian.baseFeats({
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
            ...this.zealotFeats(level)
        ]
        feats.forEach((feat) => character.addFeat(feat))
        return character
    }
}

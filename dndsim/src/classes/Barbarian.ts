import { Environment } from "../sim/Environment";
import { Operation } from "../sim/actions/Operation";
import { Character } from "../sim/Character";
import { Feat } from "../sim/Feat";
import { DamageRollEvent } from "../sim/events/DamageRollEvent";
import { AttackRollEvent } from "../sim/events/AttackRollEvent";
import { WeaponMastery } from "../sim/types";
import { WeaponMasteries } from "../feats/shared/WeaponMasteries";
import { ClassLevel } from "../sim/coreFeats/ClassLevel";
import { applyFeatSchedule, defaultMagicBonus } from "../util/helpers";
import { ExtraAttack } from "../feats/shared/ExtraAttack";
import { Resource } from "../sim/resources/Resource";
import { Greatsword } from "../weapons";
import { SavageAttacker } from "../feats/origin/SavageAttacker";
import { GreatWeaponMaster } from "../feats/general/GreatWeaponMaster";
import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement";
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense";

const RageResource = "rage"
const RageEffect = "raging"
const RecklessTag = "reckless"

class RageOperation implements Operation {
    repeatable = true;

    eligible(environment: Environment, character: Character): boolean {
        return character.hasResource(RageResource)
    }

    do(environment: Environment, character: Character): void {
        character.useResource(RageResource)
        character.addEffect(RageEffect)
    }
}

class Rage extends Feat {
    damageBonus: number

    constructor(damageBonus: number) {
        super()
        this.damageBonus = damageBonus
    }

    apply(character: Character) {
        this.addResource(character)
        character.customTurn.addOperation("before_action", new RageOperation())
        character.events.on("damage_roll", (event) => this.damageRoll(character, event))
        character.events.on("short_rest", () => this.shortRest(character))
    }

    damageRoll(character: Character, event: DamageRollEvent) {
        if (event.attack?.attack?.weapon()?.mod(character) == "str") {
            event.damage.flatDmg += this.damageBonus
        }
    }

    shortRest(character: Character) {
        character.removeEffect(RageEffect)
    }

    addResource(character: Character) {
        character.resources.set(
            RageResource,
            new Resource({
                name: RageResource,
                character,
                initialMax: 2,
                incrementOnShortRest: true,
                resetOnLongRest: true,

            })
        )
    }
}

class AddRage extends Feat {
    apply(character: Character): void {
        character.getResource(RageResource).addMax(1)
    }
}

class AddRageDamage extends Feat {
    apply(character: Character): void {
        const rageFeat = character.feats.find((feat) => feat instanceof Rage) as Rage | undefined
        if (!rageFeat) {
            return
        }
        rageFeat.damageBonus += 1
    }
}

class RecklessAttack extends Feat {
    apply(character: Character) {
        character.events.on("attack_roll", (event) => this.attackRoll(character, event))
    }

    attackRoll(character: Character, event: AttackRollEvent) {
        if (event.attack?.attack?.weapon()?.mod(character) == "str") {
            event.adv = true
            event.addTag(RecklessTag)
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
    applied = false

    apply(character: Character) {
        character.events.on("begin_turn", () => this.applied = false)
        character.events.on("damage_roll", (event) => this.damageRoll(character, event))
    }

    damageRoll(character: Character, event: DamageRollEvent) {
        if (!this.applied && event.attack?.hasTag(RecklessTag)) {
            const rageFeat = character.feats.find((feat) => feat instanceof Rage) as Rage | undefined
            if (!rageFeat) {
                return
            }
            const dice = Array(rageFeat.damageBonus).fill(6)
            event.damage.addDice(dice)
            this.applied = true
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
            feats.push(new Rage(2))
        }
        if (level >= 2) {
            feats.push(new RecklessAttack())
        }
        if (level >= 5) {
            feats.push(new ExtraAttack(2))
        }
        if (level >= 6) {
            feats.push(new AddRage())
        }
        if (level >= 9) {
            feats.push(new AddRageDamage())
        }
        if (level >= 12) {
            feats.push(new AddRage())
        }
        if (level >= 16) {
            feats.push(new AddRageDamage())
        }
        if (level >= 17) {
            feats.push(new AddRage())
        }
        if (level >= 20) {
            feats.push(new PrimalChampion())
        }
        applyFeatSchedule({
            feats,
            newFeats: asis,
            schedule: [4, 8, 12, 16, 19],
            level,
        })
        return feats
    }

    static berserkerFeats(level: number): Feat[] {
        const feats: Feat[] = []
        if (level >= 3) {
            feats.push(new Frenzy())
        }
        return feats
    }

    static createBerserkerBarbarian(level: number): Character {
        const character = new Character({
            stats: { str: 17, dex: 10, con: 16, int: 10, wis: 10, cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })

        const feats = []
        feats.push(new SavageAttacker())
        feats.push(
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
            })
        )
        feats.forEach((feat) => character.addFeat(feat))
        return character
    }
}
import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { Grappler } from "../feats/general/Grappler"
import { TavernBrawler } from "../feats/origin/TavernBrawler"
import { DefaultAttackActionOperation } from "../operations/DefaultAttackActionOperation"
import { Character } from "../sim/Character"
import { AddClassLevel } from "../sim/coreFeats/ClassLevel"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { BeginTurnEvent } from "../sim/events/BeginTurnEvent"
import { Feature } from "../sim/Feature"
import { defaultMagicBonus, unreachable } from "../util/helpers"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import {
    BaseWeaponDamageTag,
    LightWeapon,
    MartialWeapon,
    RangedWeapon,
    SimpleWeapon,
    UnarmedWeapon,
    Weapon,
} from "../sim/Weapon"
import { WeaponMastery } from "../sim/types"
import { Operation } from "../sim/actions/Operation"
import { Environment } from "../sim/Environment"
import { ExtraAttack } from "../feats/shared/ExtraAttack"
import { SetAttribute } from "../feats/shared/SetAttribute"
import { UnarmedStrike } from "../weapons/other/UnarmedStrike"
import { BeforeAttackEvent } from "../sim/events/BeforeAttackEvent"
import { FeatureGroup } from "../sim/helpers/FeatureGroup"

const FlurryTag = "flurry"

const MartialArtsDieAttribute = "martialArts"
const FlurryOfBlowsCountAttribute = "flurryOfBlowsCount"

function isUnarmedOrMonkWeapon(weapon: Weapon | undefined): boolean {
    if (!weapon) {
        return false
    }

    if (weapon.hasTag(UnarmedWeapon)) {
        return true
    }

    if (weapon.hasTag(RangedWeapon)) {
        return false
    }

    if (weapon.hasTag(SimpleWeapon)) {
        return true
    }

    if (weapon.hasTag(MartialWeapon) && weapon.hasTag(LightWeapon)) {
        return true
    }

    return false
}

class MartialArts extends Feature {
    beforeAttack(event: BeforeAttackEvent) {
        if (isUnarmedOrMonkWeapon(event.attackEvent.attack.weapon())) {
            event.attackEvent.attack.addStat("Dex")
        }
    }

    attackResult(event: AttackResultEvent) {
        const weapon = event.attack?.attack.weapon()
        if (!isUnarmedOrMonkWeapon(weapon)) {
            return
        }

        const martialArtsDie = this.character.getAttribute(
            MartialArtsDieAttribute
        )

        event.damageRolls
            .filter((damageRoll) => damageRoll.hasTag(BaseWeaponDamageTag))
            .forEach((damageRoll) => {
                if (damageRoll.dice.length == 0) {
                    // It must be doing a base 1 damage. Replace it with the martial arts die
                    damageRoll.addDice([martialArtsDie])
                    damageRoll.flatDmg -= 1
                } else {
                    damageRoll.replaceDice(
                        damageRoll.dice.map((die) =>
                            Math.max(die, martialArtsDie)
                        )
                    )
                }
            })
    }
}

class BodyAndMind extends Feature {
    apply(character: Character): void {
        character.increaseStatAndMax("Dex", 4)
        character.increaseStatAndMax("Wis", 4)
    }
}

class FlurryOfBlowsOperation implements Operation {
    repeatable: boolean = false

    constructor(private unarmedStrike: UnarmedStrike) {}

    eligible(environment: Environment, character: Character): boolean {
        return character.ki.has() && character.bonus.has()
    }

    do(environment: Environment, character: Character): void {
        character.bonus.use()
        character.ki.use()
        const numAttacks = character.getAttribute(FlurryOfBlowsCountAttribute)
        for (let i = 0; i < numAttacks; i++) {
            character.weaponAttack({
                target: environment.target,
                weapon: this.unarmedStrike,
                tags: [FlurryTag],
            })
        }
    }
}

class BonusActionAttackOperation implements Operation {
    repeatable: boolean = false

    constructor(private weapon: Weapon) {}

    eligible(environment: Environment, character: Character): boolean {
        return character.bonus.has()
    }

    do(environment: Environment, character: Character): void {
        character.bonus.use()
        character.weaponAttack({
            target: environment.target,
            weapon: this.weapon,
        })
    }
}

class OpenHandTechnique extends Feature {
    attackResult(event: AttackResultEvent): void {
        if (event.hit && event.attack.attack.hasTag(FlurryTag)) {
            if (!event.attack.target.save(this.character.dc("Wis"))) {
                event.attack.target.knockProne()
            }
        }
    }
}

class StunningStrike extends Feature {
    used: boolean = false

    constructor(private avoidOnGrapple: boolean = false) {
        super()
    }

    beginTurn(event: BeginTurnEvent): void {
        this.used = false
    }

    attackResult(event: AttackResultEvent): void {
        const character = this.character
        const target = event.attack.target
        if (
            !event.hit ||
            this.used ||
            !character.ki.has() ||
            target.hasCondition("stunned")
        ) {
            return
        }
        if (target.hasCondition("grappled") && this.avoidOnGrapple) {
            return
        }

        this.used = true
        character.ki.use()
        if (!target.save(character.dc("Wis"))) {
            target.addCondition("stunned")
            this.character.addTriggerEffect("begin_turn", (event) => {
                event.target.removeCondition("stunned")
                return "stop"
            })
        } else {
            target.addCondition("semistunned")
            this.character.addTriggerEffect("begin_turn", (event) => {
                event.target.removeCondition("semistunned")
                return "stop"
            })
        }
    }
}

class Ki extends Feature {
    constructor(private maxKi: number) {
        super()
    }

    apply(character: Character): void {
        character.ki.addMax(this.maxKi)
    }
}

class UncannyMetabolism extends Feature {
    used: boolean = false

    shortRest(): void {
        const character = this.character
        if (!this.used && character.ki.count <= character.ki.max) {
            character.ki.reset()
            this.used = true
        }
    }

    longRest(): void {
        this.used = false
    }
}

class PerfectFocus extends Feature {
    shortRest(): void {
        const character = this.character
        if (character.ki.count < 4) {
            character.ki.add(4 - character.ki.count)
        }
    }
}

type MonkSubclass = "OpenHand"

export class Monk {
    static operations = {
        BonusActionAttackOperation,
        FlurryOfBlowsOperation,
    }

    static features(args: {
        level: number
        asis: Feature[]
        masteries: WeaponMastery[]
        subclass: MonkSubclass
    }): Feature[] {
        const { level, asis, masteries, subclass } = args
        const features: Feature[] = []
        if (level >= 1) {
            features.push(Monk.level1(level, masteries))
        }
        // Level 1 (Unarmored Defense) is irrelevant
        if (level >= 2) {
            features.push(Monk.level2(level))
        }
        if (level >= 3) {
            features.push(Monk.level3(subclass))
        }
        // Level 3 (Deflect Attacks) is irrelevant/ignored
        // Level 4 (Slow Fall) is irrelevant
        if (level >= 4) {
            features.push(Monk.level4(asis[0]))
        }
        if (level >= 5) {
            features.push(Monk.level5())
        }
        // Level 6 (Empowered Strikes) is irrelevant
        // Level 7 (Evasion) is irrelevant
        if (level >= 8) {
            features.push(Monk.level8(asis[1]))
        }
        // Level 9 (Acrobatic Movement) is irrelevant
        // Level 10 (Self-Restoration) is irrelevant
        if (level >= 10) {
            features.push(Monk.level10())
        }
        if (level >= 11) {
            features.push(Monk.level11(subclass))
        }
        if (level >= 12) {
            features.push(Monk.level12(asis[2]))
        }
        // Level 13 (Deflect Energy) is irrelevant
        // Level 14 (Disciplined Survivor) is irrelevant
        if (level >= 15) {
            features.push(Monk.level15())
        }
        if (level >= 16) {
            features.push(Monk.level16(asis[3]))
        }
        if (level >= 17) {
            features.push(Monk.level17(subclass))
        }
        // Level 18 (Superior Defense) is irrelevant
        if (level >= 19) {
            features.push(Monk.level19(asis[4]))
        }
        if (level >= 20) {
            features.push(Monk.level20())
        }
        return features
    }

    static level1(level: number, masteries: WeaponMastery[]): Feature {
        return new FeatureGroup([
            new AddClassLevel("Monk", level),
            new WeaponMasteries(masteries),
            new SetAttribute(MartialArtsDieAttribute, 6),
            new MartialArts(),
        ])
    }

    static level2(level: number): Feature {
        return new FeatureGroup([
            new Ki(level),
            new UncannyMetabolism(),
            new SetAttribute(FlurryOfBlowsCountAttribute, 2),
        ])
    }

    static level3(subclass: MonkSubclass): Feature {
        if (subclass === "OpenHand") {
            return new FeatureGroup([new OpenHandTechnique()])
        } else {
            unreachable(subclass)
        }
    }

    static level4(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level5(): Feature {
        return new FeatureGroup([
            new StunningStrike(true),
            new ExtraAttack(2),
            new SetAttribute(MartialArtsDieAttribute, 8),
        ])
    }

    static level8(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level10(): Feature {
        return new FeatureGroup([new SetAttribute(FlurryOfBlowsCountAttribute, 3)])
    }

    static level11(subclass: MonkSubclass): Feature {
        if (subclass === "OpenHand") {
            // Level 11 (Fleet Step) is irrelevant
            return new FeatureGroup([new SetAttribute(MartialArtsDieAttribute, 10)])
        } else {
            unreachable(subclass)
        }
    }

    static level12(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level15(): Feature {
        return new FeatureGroup([new PerfectFocus()])
    }

    static level16(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level17(subclass: MonkSubclass): Feature {
        if (subclass === "OpenHand") {
            // TODO: Quivering Palm
            return new FeatureGroup([new SetAttribute(MartialArtsDieAttribute, 12)])
        } else {
            unreachable(subclass)
        }
    }

    static level19(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level20(): Feature {
        return new FeatureGroup([new BodyAndMind()])
    }

    static createOpenHandMonk(level: number): Character {
        const unarmedStrike = new UnarmedStrike({
            magicBonus: defaultMagicBonus(level),
        })

        const character = new Character({
            stats: { Str: 10, Dex: 17, Con: 10, Int: 10, Wis: 16, Cha: 10 },
        })

        const features: Feature[] = []
        features.push(new TavernBrawler())
        features.push(
            ...Monk.features({
                level,
                subclass: "OpenHand",
                masteries: ["Vex", "Topple"],
                asis: [
                    new Grappler("Dex"),
                    new AbilityScoreImprovement("Dex"),
                    new AbilityScoreImprovement("Wis"),
                    new AbilityScoreImprovement("Wis"),
                    new IrresistibleOffense("Dex"),
                ],
            })
        )
        features.forEach((feature) => character.addFeature(feature))

        character.customTurn.addOperation(
            "action",
            new DefaultAttackActionOperation(unarmedStrike)
        )
        if (level >= 3) {
            character.customTurn.addOperation(
                "after_action",
                new Monk.operations.FlurryOfBlowsOperation(unarmedStrike)
            )
        }
        // This is out here instead of part of level 1 so that Flurry of Blows will always
        // be prioritized over it
        character.customTurn.addOperation(
            "after_action",
            new BonusActionAttackOperation(unarmedStrike)
        )

        return character
    }
}

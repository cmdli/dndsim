import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { Grappler } from "../feats/general/Grappler"
import { TavernBrawler } from "../feats/origin/TavernBrawler"
import { DefaultAttackActionOperation } from "../sim/actions/AttackAction"
import { Character } from "../sim/Character"
import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { BeginTurnEvent } from "../sim/events/BeginTurnEvent"
import { Feat } from "../sim/Feat"
import { applyFeatSchedule, defaultMagicBonus } from "../util/helpers"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { LightWeapon, MartialWeapon, RangedWeapon, SimpleWeapon, UnarmedWeapon, Weapon } from "../sim/Weapon"
import { WeaponMastery } from "../sim/types"
import { Operation } from "../sim/actions/Operation"
import { Environment } from "../sim/Environment"
import { ExtraAttack } from "../feats/shared/ExtraAttack"
import { SetAttribute } from "../feats/shared/SetAttribute"
import { UnarmedStrike } from "../weapons/other/UnarmedStrike"
import { BeforeAttackEvent } from "../sim/events/BeforeAttackEvent"

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

class MartialArts extends Feat {
    apply(character: Character) {
        character.events.on("before_attack", (event) => this.beforeAttack(event))
        character.events.on("attack_result", (event) => this.attackResult(event))
    }

    beforeAttack(event: BeforeAttackEvent) {
        const weapon = event.attackEvent.attack.weapon()
        if (weapon && !isUnarmedOrMonkWeapon(weapon)) {
            return
        }

        event.attackEvent.attack.addStat("dex")
    }

    attackResult(event: AttackResultEvent) {
        const weapon = event.attack?.attack.weapon()
        if (!isUnarmedOrMonkWeapon(weapon)) {
            return
        }

        const martialArtsDie = this.character.getAttribute(MartialArtsDieAttribute)

        event.damageRolls
            .filter((damageRoll) => damageRoll.hasTag("base_weapon_damage"))
            .forEach((damageRoll) => {
                if (damageRoll.dice.length == 0) {
                    // It must be doing a base 1 damage. Replace it with the martial arts die
                    damageRoll.addDice([martialArtsDie])
                    damageRoll.flatDmg -= 1
                } else {
                    damageRoll.replaceDice(damageRoll.dice.map((die) => Math.max(die, martialArtsDie)))
                }
            })
    }
}

class BodyAndMind extends Feat {
    apply(character: Character): void {
        character.increaseStatAndMax("dex", 4)
        character.increaseStatAndMax("wis", 4)
    }
}

class FlurryOfBlowsOperation implements Operation {
    repeatable: boolean = false

    constructor(private unarmedStrike: UnarmedStrike) { }

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

    constructor(private weapon: Weapon) { }

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

class FlurryOfBlows extends Feat {
    constructor(private unarmedStrike: UnarmedStrike) {
        super()
    }

    apply(character: Character): void {
        character.customTurn.addOperation(
            "after_action",
            new FlurryOfBlowsOperation(this.unarmedStrike)
        )
    }
}

class OpenHandTechnique extends Feat {
    apply(character: Character): void {
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
    }

    attackResult(event: AttackResultEvent): void {
        if (event.hit && event.attack.attack.hasTag(FlurryTag)) {
            if (!event.attack.target.save(this.character.dc("wis"))) {
                event.attack.target.knockProne()
            }
        }
    }
}

class StunningStrike extends Feat {
    used: boolean = false

    constructor(private avoidOnGrapple: boolean = false) {
        super()
    }

    apply(character: Character): void {
        character.events.on("begin_turn", (event) => this.beginTurn(event))
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
    }

    beginTurn(event: BeginTurnEvent): void {
        this.used = false
        event.target.stunned = false
    }

    attackResult(event: AttackResultEvent): void {
        const character = this.character
        const target = event.attack.target
        if (!event.hit || this.used || !character.ki.has() || target.stunned) {
            return
        }
        if (target.grappled && this.avoidOnGrapple) {
            return
        }

        this.used = true
        character.ki.use()
        if (!target.save(character.dc("wis"))) {
            target.stunned = true
        } else {
            target.semistunned = true
        }
    }
}

class Ki extends Feat {

    constructor(private maxKi: number) {
        super()
    }

    apply(character: Character): void {
        character.ki.addMax(this.maxKi)
    }
}

class UncannyMetabolism extends Feat {
    used: boolean = false

    apply(character: Character): void {
        character.events.on("short_rest", () => this.shortRest())
    }

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

class PerfectFocus extends Feat {
    apply(character: Character): void {
        character.events.on("short_rest", () => this.shortRest())
    }

    shortRest(): void {
        const character = this.character
        if (character.ki.count < 4) {
            character.ki.add(4 - character.ki.count)
        }
    }
}

export class Monk {
    static baseFeats(args: {
        level: number
        asis: Array<Feat>
        masteries: WeaponMastery[],
        unarmedStrike: UnarmedStrike,
    }): Feat[] {
        const { level, asis, masteries } = args
        const feats: Feat[] = []

        if (level >= 1) {
            feats.push(new ClassLevel("Monk", level))
            feats.push(new WeaponMasteries(masteries))
            feats.push(new SetAttribute(MartialArtsDieAttribute, 6))
            feats.push(new MartialArts())
        }
        // Level 1 (Unarmored Defense) is irrelevant
        if (level >= 2) {
            feats.push(new Ki(level))
            feats.push(new UncannyMetabolism())
            feats.push(new SetAttribute(FlurryOfBlowsCountAttribute, 2))
            feats.push(new FlurryOfBlows(args.unarmedStrike))
        }
        // Level 3 (Deflect Attacks) is irrelevant/ignored
        // Level 4 (Slow Fall) is irrelevant
        if (level >= 5) {
            feats.push(new StunningStrike(true))
            feats.push(new ExtraAttack(2))
            feats.push(new SetAttribute(MartialArtsDieAttribute, 8))
        }
        // Level 6 (Empowered Strikes) is irrelevant
        // Level 7 (Evasion) is irrelevant
        // Level 9 (Acrobatic Movement) is irrelevant
        // Level 10 (Self-Restoration) is irrelevant
        if (level >= 10) {
            feats.push(new SetAttribute(FlurryOfBlowsCountAttribute, 3))
        }
        if (level >= 11) {
            feats.push(new SetAttribute(MartialArtsDieAttribute, 10))
        }
        // Level 13 (Deflect Energy) is irrelevant
        // Level 14 (Disciplined Survivor) is irrelevant
        if (level >= 15) {
            feats.push(new PerfectFocus())
        }
        if (level >= 17) {
            feats.push(new SetAttribute(MartialArtsDieAttribute, 12))
        }
        // Level 18 (Superior Defense) is irrelevant
        if (level >= 20) {
            feats.push(new BodyAndMind())
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

    static openHandFeats(level: number): Feat[] {
        const feats: Feat[] = []
        if (level >= 3) {
            feats.push(new OpenHandTechnique())
        }
        // Level 6 (Wholeness of Body) is irrelevant
        // Level 11 (Fleet Step) is irrelevant
        // Level 17 (Quivering Palm) - TODO
        return feats
    }

    static createOpenHandMonk(level: number): Character {
        const unarmedStrike = new UnarmedStrike({ magicBonus: defaultMagicBonus(level) })

        const character = new Character({
            stats: { str: 10, dex: 17, con: 10, int: 10, wis: 16, cha: 10 },
        })

        const feats: Feat[] = []
        feats.push(new TavernBrawler())

        feats.push(
            ...Monk.baseFeats({
                level,
                masteries: ["Vex", "Topple"],
                asis: [
                    new Grappler("dex"),
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("wis"),
                    new AbilityScoreImprovement("wis"),
                    new IrresistibleOffense("dex"),
                ],
                unarmedStrike,
            })
        )

        feats.push(...Monk.openHandFeats(level))

        feats.forEach((feat) => character.addFeat(feat))

        character.customTurn.addOperation(
            "action",
            new DefaultAttackActionOperation(unarmedStrike)
        )

        // This is out here instead of part of level 1 so that Flurry of Blows will always
        // be prioritized over it
        character.customTurn.addOperation("after_action", new BonusActionAttackOperation(unarmedStrike))

        return character
    }
}

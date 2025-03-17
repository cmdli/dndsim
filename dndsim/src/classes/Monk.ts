import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { Grappler } from "../feats/general/Grappler"
import { TavernBrawler } from "../feats/origin/TavernBrawler"
import { NumAttacksAttribute } from "../sim/actions/AttackAction"
import { Character } from "../sim/Character"
import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { ActionEvent } from "../sim/events/ActionEvent"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { BeginTurnEvent } from "../sim/events/BeginTurnEvent"
import { Feat } from "../sim/Feat"
import { applyFeatSchedule, rollDice } from "../util/helpers"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { FinesseWeapon, UnarmedWeapon, Weapon } from "../sim/Weapon"
import { WeaponMastery } from "../sim/types"
import { BeforeActionEvent } from "../sim/events/BeforeActionEvent"

const FlurryTag = "flurry"

function martialArtsDie(level: number): number {
    if (level >= 17) {
        return 12
    } else if (level >= 11) {
        return 10
    } else if (level >= 5) {
        return 8
    } else {
        return 6
    }
}

class BodyAndMind extends Feat {
    apply(character: Character): void {
        character.increaseStatMax("dex", 4)
        character.increaseStatMax("wis", 4)
        character.increaseStat("dex", 4)
        character.increaseStat("wis", 4)
    }
}

class FlurryOfBlows extends Feat {
    numAttacks: number
    weapon: Weapon

    constructor(numAttacks: number, weapon: Weapon) {
        super()
        this.numAttacks = numAttacks
        this.weapon = weapon
    }

    apply(character: Character): void {
        character.events.on("before_action", (event) =>
            this.beforeAction(event)
        )
    }

    beforeAction(event: BeforeActionEvent): void {
        const character = this.character!
        const target = event.target
        if (!target) {
            return
        }

        if (character.ki.has() && character.bonus.use("FlurryOfBlows")) {
            character.ki.use()
            for (let i = 0; i < this.numAttacks; i++) {
                character.weaponAttack({
                    target,
                    weapon: this.weapon,
                    tags: [FlurryTag],
                })
            }
        } else if (character.bonus.use("MonkBonusAttack")) {
            character.weaponAttack({
                target,
                weapon: this.weapon,
            })
        }
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
            if (!event.attack.target.save(this.character!.dc("wis"))) {
                event.attack.target.knockProne()
            }
        }
    }
}

class StunningStrike extends Feat {
    weaponDie: number
    used: boolean = false
    avoidOnGrapple: boolean

    constructor(level: number, avoidOnGrapple: boolean = false) {
        super()
        this.weaponDie = martialArtsDie(level)
        this.avoidOnGrapple = avoidOnGrapple
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
        const character = this.character!
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
    maxKi: number

    constructor(maxKi: number) {
        super()
        this.maxKi = maxKi
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
        const character = this.character!
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
        const character = this.character!
        if (character.ki.count < 4) {
            character.ki.add(4 - character.ki.count)
        }
    }
}

class Fists extends Weapon {
    constructor(args: { weaponDie: number; magicBonus?: number }) {
        super({
            name: "Fists",
            numDice: 1,
            die: args.weaponDie,
            magicBonus: args.magicBonus,
            tags: [FinesseWeapon, UnarmedWeapon],
        })
    }
}

class MonkAction extends Feat {
    weapon: Weapon

    constructor(weapon: Weapon) {
        super()
        this.weapon = weapon
    }

    apply(character: Character): void {
        character.events.on("action", (data) => this.action(data))
    }

    action(data: ActionEvent): void {
        const numAttacks = this.character!.hasClassLevel("Monk", 5) ? 2 : 1

        for (let i = 0; i < numAttacks; i++) {
            this.character!.weaponAttack({
                target: data.target,
                weapon: this.weapon,
                tags: ["main_action"],
            })
        }
    }
}

export class Monk {
    static baseFeats(args: {
        level: number
        asis: Array<Feat>
        masteries: WeaponMastery[]
    }): Feat[] {
        const { level, asis, masteries } = args
        const feats: Feat[] = []

        if (level >= 1) {
            feats.push(new ClassLevel("Monk", level))
            feats.push(new WeaponMasteries(masteries))
        }
        // Level 1 (Unarmored Defense) is irrelevant
        if (level >= 2) {
            feats.push(new Ki(level))
            feats.push(new UncannyMetabolism())
        }
        // Level 3 (Deflect Attacks) is irrelevant/ignored
        // Level 4 (Slow Fall) is irrelevant
        if (level >= 5) {
            feats.push(new StunningStrike(level, true))
        }
        // Level 6 (Empowered Strikes) is irrelevant
        // Level 7 (Evasion) is irrelevant
        // Level 9 (Acrobatic Movement) is irrelevant
        // Level 10 (Self-Restoration) is irrelevant
        // Level 13 (Deflect Energy) is irrelevant
        // Level 14 (Disciplined Survivor) is irrelevant
        if (level >= 15) {
            feats.push(new PerfectFocus())
        }
        // Level 18 (Superior Defense) is irrelevant
        if (level >= 20) {
            feats.push(new BodyAndMind())
        }
        applyFeatSchedule({
            feats,
            newFeats: asis,
            schedule: [4, 8, 12, 16, 19],
            level,
        })
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
        const character = new Character({
            stats: { str: 10, dex: 17, con: 10, int: 10, wis: 16, cha: 10 },
        })

        const weaponDie = martialArtsDie(level)
        const magicBonus = Math.floor(level / 4)
        const fists = new Fists({ weaponDie, magicBonus })

        const feats: Feat[] = []
        feats.push(new TavernBrawler())
        feats.push(new MonkAction(fists))

        // Add flurry of blows
        const numFlurryAttacks = level >= 10 ? 3 : 2
        feats.push(new FlurryOfBlows(numFlurryAttacks, fists))

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
            })
        )

        feats.push(...Monk.openHandFeats(level))

        feats.forEach((feat) => character.addFeat(feat))

        return character
    }
}

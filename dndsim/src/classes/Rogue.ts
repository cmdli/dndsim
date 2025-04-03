import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { Character } from "../sim/Character"
import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { ActionEvent } from "../sim/events/ActionEvent"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { Feat } from "../sim/Feat"
import { applyFeatSchedule, rollDice } from "../util/helpers"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { Weapon } from "../sim/Weapon"
import { WeaponMastery } from "../sim/types"
import { Shortsword, Scimitar, Rapier } from "../weapons/index"

class SneakAttack extends Feat {
    used: boolean = false

    apply(character: Character): void {
        character.events.on("begin_turn", () => this.beginTurn())
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
    }

    beginTurn(): void {
        this.used = false
    }

    attackResult(event: AttackResultEvent): void {
        if (event.hit && !this.used) {
            this.used = true
            const level = this.character.getClassLevel("Rogue")
            const diceCount = Math.ceil(level / 2)
            event.addDamage({
                source: "SneakAttack",
                dice: Array(diceCount).fill(6),
            })
        }
    }
}

class SteadyAim extends Feat {
    enabled: boolean = false

    apply(character: Character): void {
        character.events.on("before_action", () => this.beforeAction())
        character.events.on("attack_roll", (event) => this.attackRoll(event))
        character.events.on("end_turn", () => this.endTurn())
    }

    beforeAction(): void {
        if (this.character.bonus.use("SteadyAim")) {
            this.enabled = true
        }
    }

    attackRoll(event: AttackRollEvent): void {
        if (this.enabled) {
            event.adv = true
            this.enabled = false
        }
    }

    endTurn(): void {
        this.enabled = false
    }
}

class StrokeOfLuck extends Feat {
    used: boolean = false

    apply(character: Character): void {
        character.events.on("begin_turn", () => this.beginTurn())
        character.events.on("attack_roll", (event) => this.attackRoll(event))
    }

    beginTurn(): void {
        this.used = false
    }

    attackRoll(event: AttackRollEvent): void {
        if (!this.used && event.roll() < 10) {
            this.used = true
            event.roll1 = 20
            event.roll2 = 20
        }
    }
}

class Assassinate extends Feat {
    firstTurn: boolean = true
    usedDmg: boolean = false
    adv: boolean = false
    level: number

    constructor(level: number) {
        super()
        this.level = level
    }

    apply(character: Character): void {
        character.events.on("short_rest", () => this.shortRest())
        character.events.on("begin_turn", () => this.beginTurn())
        character.events.on("attack_roll", (event) => this.attackRoll(event))
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
        character.events.on("end_turn", () => this.endTurn())
    }

    shortRest(): void {
        this.firstTurn = true
        this.usedDmg = false
    }

    beginTurn(): void {
        if (this.firstTurn) {
            // Simulate the initiative check
            const rogueRoll =
                Math.max(rollDice(1, 20), rollDice(1, 20)) +
                this.character.mod("dex")
            const enemyRoll = rollDice(1, 20)
            if (rogueRoll > enemyRoll) {
                this.adv = true
            }
        }
    }

    attackRoll(event: AttackRollEvent): void {
        if (this.adv) {
            event.adv = true
        }
    }

    attackResult(event: AttackResultEvent): void {
        if (event.hit && this.firstTurn && !this.usedDmg) {
            this.usedDmg = true
            event.addDamage({
                source: "Assassinate",
                flatDmg: this.level,
            })
        }
    }

    endTurn(): void {
        this.adv = false
        this.firstTurn = false
    }
}

class DeathStrike extends Feat {
    enabled: boolean = false

    apply(character: Character): void {
        character.events.on("short_rest", () => this.shortRest())
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
        character.events.on("end_turn", () => this.endTurn())
    }

    shortRest(): void {
        this.enabled = true
    }

    attackResult(event: AttackResultEvent): void {
        if (event.hit && this.enabled) {
            this.enabled = false
            if (!event.attack.target.save(this.character.dc("dex"))) {
                event.dmgMultiplier *= 2
            }
        }
    }

    endTurn(): void {
        this.enabled = false
    }
}

class BoomingBladeAction extends Feat {
    weapon: Weapon

    constructor(weapon: Weapon) {
        super()
        this.weapon = weapon
    }

    apply(character: Character): void {
        character.events.on("action", (data) => this.action(data))
        character.events.on("attack_result", (event) =>
            this.attackResult(event)
        )
    }

    action(data: ActionEvent): void {
        this.character.weaponAttack({
            target: data.target,
            weapon: this.weapon,
            tags: ["main_action", "booming_blade"],
        })
    }

    attackResult(event: AttackResultEvent): void {
        if (!event.hit || !event.attack.attack.hasTag("booming_blade")) {
            return
        }

        let extraDice = 0
        const level = this.character.level
        if (level >= 17) {
            extraDice = 3
        } else if (level >= 11) {
            extraDice = 2
        } else if (level >= 5) {
            extraDice = 1
        } else {
            return
        }

        event.addDamage({
            source: "BoomingBlade",
            dice: Array(extraDice).fill(8),
        })
    }
}

class RogueAction extends Feat {
    weapon: Weapon
    nickWeapon?: Weapon

    constructor(args: { weapon: Weapon; nickWeapon?: Weapon }) {
        super()
        this.weapon = args.weapon
        this.nickWeapon = args.nickWeapon
    }

    apply(character: Character): void {
        character.events.on("action", (data) => this.action(data))
    }

    action(data: ActionEvent): void {
        this.character.weaponAttack({
            target: data.target,
            weapon: this.weapon,
            tags: ["main_action"],
        })

        if (this.nickWeapon) {
            this.character.weaponAttack({
                target: data.target,
                weapon: this.nickWeapon,
                tags: ["light"],
            })
        }
    }
}

export class Rogue {
    static baseFeats(args: {
        level: number
        asis: Array<Feat>
        masteries: WeaponMastery[]
    }): Feat[] {
        const { level, asis, masteries } = args
        const feats: Feat[] = []
        if (level >= 1) {
            feats.push(new ClassLevel("Rogue", level))
            feats.push(new SneakAttack())
            feats.push(new WeaponMasteries(masteries))
        }
        // Level 2 (Cunning Action) is irrelevant for now
        if (level >= 3) {
            feats.push(new SteadyAim())
        }
        // Level 5 (Cunning Strike) is mostly useless for DPR
        // Level 7 (Evasion) is irrelevant
        // Level 7 (Reliable Talent) is irrelevant
        // Level 11 (Improved Cunning Strike) is unused
        // Level 14 (Devious Strikes) is unused
        // Level 15 (Slippery Mind) is irrelevant
        // Level 18 (Elusive) is irrelevant
        if (level >= 20) {
            feats.push(new StrokeOfLuck())
        }
        applyFeatSchedule({
            feats,
            newFeats: asis,
            schedule: [4, 8, 10, 12, 16, 19],
            level,
        })
        return feats
    }

    static assassinFeats(level: number): Feat[] {
        const feats: Feat[] = []
        if (level >= 3) {
            feats.push(new Assassinate(level))
        }
        // Level 3 (Assassin's Tools) is irrelevant
        // Level 9 (Infiltration Expertise) is irrelevant
        // TODO: Level 13 (Envenom Weapons)
        if (level >= 17) {
            feats.push(new DeathStrike())
        }
        return feats
    }

    static createAssassinRogue(
        level: number,
        useBoomingBlade: boolean = false
    ): Character {
        const character = new Character({
            stats: { str: 10, dex: 17, con: 10, int: 10, wis: 10, cha: 10 },
        })
        let feats: Feat[] = []
        if (level >= 5 && useBoomingBlade) {
            const rapier = new Rapier()
            feats.push(new BoomingBladeAction(rapier))
        } else {
            const shortsword = new Shortsword()
            const scimitar = new Scimitar()
            feats.push(
                new RogueAction({
                    weapon: shortsword,
                    nickWeapon: scimitar,
                })
            )
        }
        feats.push(
            ...Rogue.baseFeats({
                level,
                masteries: ["Vex", "Nick"],
                asis: [
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex", "wis"),
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex"),
                    new IrresistibleOffense("dex"),
                ],
            })
        )
        feats.push(...Rogue.assassinFeats(level))
        feats.forEach((feat) => character.addFeat(feat))
        return character
    }

    static createArcaneTricksterRogue(level: number): Character {
        const character = new Character({
            stats: { str: 10, dex: 17, con: 10, int: 10, wis: 10, cha: 10 },
        })
        let feats: Feat[] = []
        if (level >= 5) {
            const rapier = new Rapier()
            feats.push(new BoomingBladeAction(rapier))
        } else {
            const shortsword = new Shortsword()
            const scimitar = new Scimitar()
            feats.push(
                new RogueAction({
                    weapon: shortsword,
                    nickWeapon: scimitar,
                })
            )
        }
        feats = feats.concat(
            Rogue.baseFeats({
                level,
                masteries: ["Vex", "Nick"],
                asis: [
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex", "wis"),
                    new AbilityScoreImprovement("dex"),
                    new AbilityScoreImprovement("dex"),
                    new IrresistibleOffense("dex"),
                ],
            })
        )
        // TODO: Arcane Trickster specific feats
        feats.forEach((feat) => character.addFeat(feat))
        return character
    }
}

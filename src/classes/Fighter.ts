import { GreatWeaponFighting } from "../feats/fightingStyle/GreatWeaponFighting"
import { AbilityScoreImprovement } from "../feats/general/AbilityScoreImprovement"
import { GreatWeaponMaster } from "../feats/general/GreatWeaponMaster"
import { IrresistibleOffense } from "../feats/epic/IrresistibleOffense"
import { SavageAttacker } from "../feats/origin/SavageAttacker"
import { ExtraAttack } from "../feats/shared/ExtraAttack"
import { ImprovedCritical } from "../feats/shared/ImprovedCritical"
import { WeaponMasteries } from "../feats/shared/WeaponMasteries"
import { Character } from "../sim/Character"
import { Environment } from "../sim/Environment"
import { AddClassLevel } from "../sim/coreFeats/ClassLevel"
import { AttackResultEvent } from "../sim/events/AttackResultEvent"
import { AttackRollEvent } from "../sim/events/AttackRollEvent"
import { BeginTurnEvent } from "../sim/events/BeginTurnEvent"
import { Feature } from "../sim/Feature"
import {
    AttackActionTag,
    MainActionTag,
    NumAttacksAttribute,
} from "../sim/actions/AttackAction"
import { ActionOperation } from "../sim/actions/ActionOperation"
import { Operation } from "../sim/actions/Operation"
import { Resource } from "../sim/resources/Resource"
import { WeaponMastery } from "../sim/types"
import { Weapon } from "../sim/Weapon"
import { defaultMagicBonus, unreachable } from "../util/helpers"
import { Greatsword } from "../weapons/martial/melee/Greatsword"
import { Maul } from "../weapons/martial/melee/Maul"
import { FeatureGroup } from "../sim/helpers/FeatureGroup"

type FighterSubclass = "Champion" | "Battlemaster"

const ActionSurgeResource = "ActionSurge"

class AddActionSurge extends Feature {
    apply(character: Character): void {
        if (!character.resources.has(ActionSurgeResource)) {
            character.resources.set(
                ActionSurgeResource,
                new Resource({
                    name: ActionSurgeResource,
                    character,
                    initialMax: 1,
                    resetOnShortRest: true,
                })
            )
        }
        character.getResource(ActionSurgeResource).addMax(1)
    }
}

class StudiedAttacks extends Feature {
    enabled = false

    attackRoll(event: AttackRollEvent): void {
        if (this.enabled) {
            event.adv = true
            this.enabled = false
        }
    }

    attackResult(event: AttackResultEvent): void {
        if (!event.hit) {
            this.enabled = true
        }
    }
}

class HeroicAdvantage extends Feature {
    beginTurn(_event: BeginTurnEvent): void {
        this.character.heroicInspiration.add(1)
    }

    attackRoll(event: AttackRollEvent): void {
        if (event.adv || !this.character.heroicInspiration.has()) {
            return
        }

        if (event.roll1 < 8) {
            this.character.heroicInspiration.use()
            event.adv = true
        }
    }
}

class PrecisionAttack extends Feature {
    constructor(private low: number) {
        super()
    }

    attackRoll(event: AttackRollEvent): void {
        if (
            event.attack.hasTag("used_maneuver") ||
            !this.character.combatSuperiority.has() ||
            event.hits()
        ) {
            return
        }

        if (event.roll() >= this.low) {
            const roll = this.character.combatSuperiority.roll()
            event.situationalBonus += roll
            event.attack.addTag("used_maneuver")
        }
    }
}

class AddCombatSuperiorityDice extends Feature {
    constructor(
        private count: number,
        private die: number
    ) {
        super()
    }

    apply(character: Character): void {
        for (let i = 0; i < this.count; i++) {
            character.combatSuperiority.addDie(this.die)
        }
    }
}

class UpgradeCombatSuperiorityDice extends Feature {
    constructor(private die: number) {
        super()
    }

    apply(character: Character): void {
        character.combatSuperiority.maxDice =
            character.combatSuperiority.maxDice.map(() => this.die)
        character.combatSuperiority.dice = character.combatSuperiority.dice.map(
            () => this.die
        )
    }
}

class Relentless extends Feature {
    apply(character: Character): void {
        character.combatSuperiority.enableRelentless()
    }
}

class ActionSurgeOperation implements Operation {
    repeatable: boolean = false

    eligible(environment: Environment): boolean {
        return environment.character.hasResource(ActionSurgeResource)
    }

    do(environment: Environment): void {
        environment.character.useResource(ActionSurgeResource)
        environment.character.actions.add(1, true)
    }
}

class ToppleIfNecessaryAttackAction extends ActionOperation {
    repeatable: boolean = true
    weapon: Weapon
    toppleWeapon: Weapon

    constructor(weapon: Weapon, toppleWeapon: Weapon) {
        super()
        this.weapon = weapon
        this.toppleWeapon = toppleWeapon
    }

    action(environment: Environment): void {
        const target = environment.target
        const character = environment.character
        const numAttacks = character.getAttribute(NumAttacksAttribute)
        for (let i = 0; i < numAttacks; i++) {
            let weapon = this.weapon
            if (!target.hasCondition("prone") && i < numAttacks - 1) {
                weapon = this.toppleWeapon
            }
            character.weaponAttack({
                target,
                weapon,
                tags: [MainActionTag, AttackActionTag],
            })
        }
    }
}

export class Fighter {
    static operations = {
        ActionSurgeOperation,
        ToppleIfNecessaryAttackAction,
    }

    static features(args: {
        level: number
        asis: Array<Feature>
        masteries: WeaponMastery[]
        fightingStyle: Feature
        subclass: FighterSubclass
    }): Feature[] {
        const { level, asis, masteries, fightingStyle, subclass } = args
        const features: Feature[] = []
        if (level >= 1) {
            features.push(Fighter.level1(level, masteries, fightingStyle))
        }
        if (level >= 2) {
            features.push(Fighter.level2())
        }
        if (level >= 3) {
            features.push(Fighter.level3(subclass))
        }
        if (level >= 4) {
            features.push(Fighter.level4(asis[0]))
        }
        if (level >= 5) {
            features.push(Fighter.level5())
        }
        if (level >= 6) {
            features.push(Fighter.level6(asis[1]))
        }
        if (level >= 7) {
            features.push(Fighter.level7(subclass))
        }
        if (level >= 8) {
            features.push(Fighter.level8(asis[2]))
        }
        if (level >= 9) {
            features.push(Fighter.level9())
        }
        if (level >= 10) {
            features.push(Fighter.level10(subclass))
        }
        if (level >= 11) {
            features.push(Fighter.level11())
        }
        if (level >= 12) {
            features.push(Fighter.level12(asis[3]))
        }
        if (level >= 13) {
            features.push(Fighter.level13())
        }
        if (level >= 14) {
            features.push(Fighter.level14(asis[4]))
        }
        if (level >= 15) {
            features.push(Fighter.level15(subclass))
        }
        if (level >= 16) {
            features.push(Fighter.level16(asis[5]))
        }
        if (level >= 17) {
            features.push(Fighter.level17())
        }
        if (level >= 18) {
            features.push(Fighter.level18(subclass))
        }
        if (level >= 19) {
            features.push(Fighter.level19(asis[6]))
        }
        if (level >= 20) {
            features.push(Fighter.level20())
        }
        return features
    }

    static createBattlemasterFighter(level: number): Character {
        const character = new Character({
            stats: { Str: 17, Dex: 10, Con: 10, Int: 10, Wis: 10, Cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })
        const toppleWeapon = new Maul({ magicBonus: defaultMagicBonus(level) })
        const features: Feature[] = []
        features.push(new SavageAttacker())
        features.push(
            ...Fighter.features({
                level,
                asis: [
                    new GreatWeaponMaster(weapon),
                    new AbilityScoreImprovement("Str"),
                    new AbilityScoreImprovement("Con"),
                    new AbilityScoreImprovement("Con"),
                    new AbilityScoreImprovement("Con"),
                    new AbilityScoreImprovement("Con"),
                    new IrresistibleOffense("Str"),
                ],
                masteries: ["Topple", "Graze"],
                fightingStyle: new GreatWeaponFighting(),
                subclass: "Battlemaster",
            })
        )
        character.customTurn.addOperation(
            "before_action",
            new ActionSurgeOperation()
        )
        character.customTurn.addOperation(
            "action",
            new ToppleIfNecessaryAttackAction(weapon, toppleWeapon)
        )
        features.forEach((feature) => character.addFeature(feature))
        return character
    }

    static createChampionFighter(level: number): Character {
        const character = new Character({
            stats: { Str: 17, Dex: 10, Con: 10, Int: 10, Wis: 10, Cha: 10 },
        })
        const weapon = new Greatsword({ magicBonus: defaultMagicBonus(level) })
        const toppleWeapon = new Maul({ magicBonus: defaultMagicBonus(level) })
        const features: Feature[] = []
        features.push(new SavageAttacker())
        features.push(
            ...Fighter.features({
                level,
                asis: [
                    new GreatWeaponMaster(weapon),
                    new AbilityScoreImprovement("Str"),
                    new AbilityScoreImprovement("Con"),
                    new AbilityScoreImprovement("Con"),
                    new AbilityScoreImprovement("Con"),
                    new AbilityScoreImprovement("Con"),
                    new IrresistibleOffense("Str"),
                ],
                masteries: ["Graze", "Topple"],
                fightingStyle: new GreatWeaponFighting(),
                subclass: "Champion",
            })
        )
        character.customTurn.addOperation(
            "before_action",
            new ActionSurgeOperation()
        )
        character.customTurn.addOperation(
            "action",
            new ToppleIfNecessaryAttackAction(weapon, toppleWeapon)
        )
        features.forEach((feature) => character.addFeature(feature))
        return character
    }

    static level1(
        level: number,
        weaponMasteries: WeaponMastery[],
        fightingStyle: Feature
    ): Feature {
        return new FeatureGroup([
            new AddClassLevel("Fighter", level),
            new WeaponMasteries(weaponMasteries),
            fightingStyle,
        ])
    }

    static level2(): Feature {
        return new FeatureGroup([new AddActionSurge()])
    }

    static level3(subclass: FighterSubclass): Feature {
        if (subclass === "Champion") {
            return new FeatureGroup([new ImprovedCritical(19)])
        } else if (subclass === "Battlemaster") {
            return new FeatureGroup([
                new AddCombatSuperiorityDice(4, 8),
                new PrecisionAttack(8),
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

    static level6(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level7(subclass: FighterSubclass): Feature {
        if (subclass === "Battlemaster") {
            return new FeatureGroup([new AddCombatSuperiorityDice(1, 8)])
        } else if (subclass === "Champion") {
            // No-op
            return new FeatureGroup([])
        } else {
            unreachable(subclass)
        }
    }

    static level8(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level9(): Feature {
        return new FeatureGroup([])
    }

    static level10(subclass: FighterSubclass): Feature {
        if (subclass === "Champion") {
            return new FeatureGroup([new HeroicAdvantage()])
        } else if (subclass === "Battlemaster") {
            return new FeatureGroup([new UpgradeCombatSuperiorityDice(10)])
        } else {
            unreachable(subclass)
        }
    }

    static level11(): Feature {
        return new FeatureGroup([new ExtraAttack(3)])
    }

    static level12(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level13(): Feature {
        return new FeatureGroup([new StudiedAttacks()])
    }

    static level14(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level15(subclass: FighterSubclass): Feature {
        if (subclass === "Champion") {
            return new FeatureGroup([new ImprovedCritical(18)])
        } else if (subclass === "Battlemaster") {
            return new FeatureGroup([
                new AddCombatSuperiorityDice(1, 10),
                new Relentless(),
            ])
        }
        return new FeatureGroup([])
    }

    static level16(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level17(): Feature {
        return new FeatureGroup([new AddActionSurge()])
    }

    static level18(subclass: FighterSubclass): Feature {
        if (subclass === "Battlemaster") {
            return new FeatureGroup([new UpgradeCombatSuperiorityDice(12)])
        }
        return new FeatureGroup([])
    }

    static level19(asi: Feature): Feature {
        return new FeatureGroup([asi])
    }

    static level20(): Feature {
        return new FeatureGroup([new ExtraAttack(4)])
    }
}

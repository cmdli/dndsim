import {
    CharacterEventMapping,
    CharacterEventName,
} from "./events/CharacterEvent"
import { Feature } from "./Feature"
import { EventLoop } from "../util/EventLoop"
import { Class, Stat, StatOrNone, WeaponMastery } from "./types"
import { Resource } from "./resources/Resource"
import { Target } from "./Target"
import { Weapon } from "./Weapon"
import { Attack, WeaponAttack } from "./Attack"
import { DamageRoll } from "./helpers/DamageRoll"
import { Spellcasting } from "./spells/Spellcasting"
import { Spell } from "./spells/Spell"
import { AttackEvent } from "./events/AttackEvent"
import { AttackResultEvent } from "./events/AttackResultEvent"
import { AttackRollEvent } from "./events/AttackRollEvent"
import { DamageRollEvent } from "./events/DamageRollEvent"
import { BeforeAttackEvent } from "./events/BeforeAttackEvent"
import { ShortRestEvent } from "./events/ShortRestEvent"
import { LongRestEvent } from "./events/LongRestEvent"
import { EnemyTurnEvent } from "./events/EnemyTurnEvent"
import { NumAttacksAttribute } from "./actions/AttackAction"
import { Graze } from "./coreFeats/Graze"
import { Topple } from "./coreFeats/Topple"
import { Vex } from "./coreFeats/Vex"
import { log } from "../util/Log"
import { CombatSuperiority } from "./resources/CombatSuperiority"
import { CustomTurn } from "./actions/CustomTurn"
import { Environment } from "./Environment"
import { Effect } from "./Effect"

const DEFAULT_STAT_MAX = 20

export class Character {
    // Stats
    level: number = 0
    stats: Record<StatOrNone, number>
    statMax: Record<Stat, number> = {
        str: DEFAULT_STAT_MAX,
        dex: DEFAULT_STAT_MAX,
        con: DEFAULT_STAT_MAX,
        int: DEFAULT_STAT_MAX,
        wis: DEFAULT_STAT_MAX,
        cha: DEFAULT_STAT_MAX,
    }

    features: Array<Feature> = []
    events: EventLoop<CharacterEventName, CharacterEventMapping> =
        new EventLoop()
    effects: Map<string, Effect> = new Map()
    minions: Set<Character> = new Set()

    spells: Spellcasting = new Spellcasting(this)
    masteries: Set<WeaponMastery> = new Set()
    classLevels: Map<Class, number> = new Map()
    attributes: Map<string, number> = new Map([[NumAttacksAttribute, 1]])

    // Resources
    bonus = new Resource({
        name: "Bonus",
        character: this,
        initialMax: 1,
    })
    actions = new Resource({
        name: "Action",
        character: this,
        initialMax: 1,
    })
    combatSuperiority: CombatSuperiority = new CombatSuperiority(this)
    heroicInspiration = new Resource({
        name: "HeroicInspiration",
        character: this,
        initialMax: 1,
    })
    ki = new Resource({
        name: "Ki",
        character: this,
        resetOnLongRest: true,
    })
    resources: Map<string, Resource> = new Map()
    // TODO: Add other class resources
    // TODO: Handle actions better
    grappleStat: StatOrNone = "str"
    customTurn: CustomTurn = new CustomTurn()

    constructor(args: { stats: Omit<Record<Stat, number>, "none"> }) {
        const { stats } = args
        this.stats = { ...stats, none: 10 }
        for (const feature of [new Graze(), new Topple(), new Vex()]) {
            this.addFeature(feature)
        }
    }

    addFeature(feature: Feature): void {
        this.features.push(feature)
        feature.internalApply(this)
    }

    stat(stat: StatOrNone): number {
        return this.stats[stat]
    }

    mod(stat: StatOrNone): number {
        return Math.floor((this.stat(stat) - 10) / 2)
    }

    increaseStatMax(stat: Stat, amount: number): void {
        this.statMax[stat] += amount
    }

    increaseStat(stat: Stat, amount: number): void {
        this.stats[stat] += amount
        if (this.stats[stat] > this.statMax[stat]) {
            this.stats[stat] = this.statMax[stat]
        }
    }

    increaseStatAndMax(stat: Stat, amount: number) {
        this.increaseStatMax(stat, amount)
        this.increaseStat(stat, amount)
    }

    dc(stat: StatOrNone): number {
        return this.mod(stat) + this.prof() + 8
    }

    prof(): number {
        return Math.floor((this.level - 1) / 4) + 2
    }

    addMinion(minion: Character): void {
        this.minions.add(minion)
    }

    removeMinion(minion: Character): void {
        this.minions.delete(minion)
    }

    hasEffect(effect: string): boolean {
        return this.effects.has(effect)
    }

    addEffect(effect: Effect): void {
        this.effects.set(effect.name, effect)
        effect.internalApply(this)
    }

    removeEffect(effect: string): void {
        if (this.effects.has(effect)) {
            this.effects.get(effect)?.end(this)
            this.effects.delete(effect)
        }
    }

    getAttribute(attribute: string): number {
        return this.attributes.get(attribute) ?? 0
    }

    setAttribute(attribute: string, value: number): void {
        this.attributes.set(attribute, value)
    }

    getClassLevel(class_: Class): number {
        return this.classLevels.get(class_) ?? 0
    }

    hasClassLevel(class_: Class, level: number): boolean {
        return (this.getClassLevel(class_) ?? 0) >= level
    }

    addClassLevel(class_: Class, level: number): void {
        this.classLevels.set(class_, this.getClassLevel(class_) + level)
        this.level += level
    }

    getResource(name: string): Resource {
        if (!this.resources.has(name)) {
            this.resources.set(
                name,
                new Resource({
                    name,
                    character: this,
                    initialMax: 0,
                })
            )
        }
        return this.resources.get(name)!
    }

    hasResource(name: string, amount: number = 1): boolean {
        return this.resources.get(name)?.has(amount) ?? false
    }

    useResource(name: string, amount: number = 1) {
        this.getResource(name).use(amount)
    }

    // Adds a recurring effect on a particular event. If the effect function returns true, the effect is removed.
    addTriggerEffect<Event extends CharacterEventName>(
        trigger: Event,
        effect: (event: CharacterEventMapping[Event]) => "continue" | "stop"
    ): void {
        const listener = (event: CharacterEventMapping[Event]) => {
            if (effect(event) === "stop") {
                this.events.removeListener(trigger, listener)
            }
        }
        this.events.on(trigger, listener)
    }

    // =============================
    //       COMMON ACTIONS
    // =============================

    grapple(target: Target): void {
        if (target.save(this.dc(this.grappleStat))) {
            target.grapple()
        }
    }

    // =============================
    //       LIFECYCLE EVENTS
    // =============================

    turn(target: Target): void {
        log.record("Turn", 1)
        this.actions.reset()
        this.bonus.reset()
        this.customTurn.doTurn(
            new Environment({ character: this, target }),
            this
        )
        for (const minion of this.minions) {
            minion.turn(target)
        }
    }

    shortRest(): void {
        this.events.emit("short_rest", new ShortRestEvent())
        for (const effect of this.effects.keys()) {
            if (this.effects.get(effect)?.duration === "until_short_rest") {
                this.removeEffect(effect)
            }
        }
    }

    longRest(): void {
        this.shortRest()
        this.events.emit("long_rest", new LongRestEvent())
    }

    enemyTurn(target: Target): void {
        this.events.emit("enemy_turn", new EnemyTurnEvent({ target }))
    }

    // =============================
    //       WEAPON EVENTS
    // =============================

    weaponAttack(args: {
        target: Target
        weapon: Weapon
        tags?: string[]
        onResult?: (event: AttackResultEvent) => void
    }): void {
        const attack = new WeaponAttack({
            weapon: args.weapon,
            tags: args.tags,
            onResult: args.onResult,
        })
        this.attack({ target: args.target, attack })
    }

    attack(args: { target: Target; attack: Attack }): void {
        const { target, attack } = args
        log.record(`Attack (${attack.name()})`, 1)
        const attackData = new AttackEvent({ target, attack })
        this.events.emit("before_attack", new BeforeAttackEvent(attackData))
        const toHit = attack.toHit(this)
        const rollResult = this.attackRoll(attackData, toHit)

        if (rollResult.hits()) {
            log.record(`Hit (${attack.name()})`, 1)
        } else {
            log.record(`Miss (${attack.name()})`, 1)
        }
        if (rollResult.isCrit()) {
            log.record(`Crit (${attack.name()})`, 1)
        }

        const attackResult = new AttackResultEvent({
            attack: attackData,
            hit: rollResult.hits(),
            crit: rollResult.isCrit(),
            roll: rollResult.roll(),
        })
        args.attack.attackResult(attackResult, this)
        this.events.emit("attack_result", attackResult)
        for (const damage of attackResult.damageRolls) {
            if (rollResult.isCrit()) {
                damage.dice = damage.dice.concat(damage.dice)
            }
            this.doDamage({
                target,
                damage,
                attack: attackData,
                multiplier: attackResult.dmgMultiplier,
            })
        }
    }

    attackRoll(attackData: AttackEvent, toHit: number): AttackRollEvent {
        const { target, attack } = attackData
        const data = new AttackRollEvent({ attack: attackData, toHit })
        if (target.hasCondition("prone")) {
            if (attack.isRanged()) {
                data.disadv = true
            } else {
                data.adv = true
            }
        }
        if (target.hasCondition("stunned")) {
            data.adv = true
        }
        this.events.emit("attack_roll", data)
        return data
    }

    doDamage(args: {
        target: Target
        damage: DamageRoll
        attack?: AttackEvent
        multiplier?: number
        spell?: Spell
    }): void {
        const { target, damage, attack, spell } = args
        const multiplier = args.multiplier ?? 1
        const damageData = new DamageRollEvent({
            target,
            damage,
            attack,
            spell,
        })
        this.events.emit("damage_roll", damageData)
        target.addDamage(
            damage.source,
            damage.type,
            Math.floor(damage.total() * multiplier)
        )
    }
}

import {
    CharacterEvent,
    CharacterEventData,
    CharacterEventMapping,
    CharacterEventName,
} from "./events/CharacterEvent"
import { Feat } from "./Feat"
import { EventLoop } from "../util/EventLoop"
import { Class, Stat, WeaponMastery } from "./types"
import { Resource } from "./Resource"
import { Target } from "./Target"
import { Weapon } from "./Weapon"
import { Attack, WeaponAttack } from "./Attack"
import { DamageRoll } from "./helpers/DamageRoll"
import { Spellcasting } from "./spells/Spellcasting"
import { Spell } from "./spells/Spell"
import { ActionEvent } from "./events/ActionEvent"
import { AttackEvent } from "./events/AttackEvent"
import { AttackResultEvent } from "./events/AttackResultEvent"
import { AttackRollEvent } from "./events/AttackRollEvent"
import { DamageRollEvent } from "./events/DamageRollEvent"

const DEFAULT_STAT_MAX = 20

export class Character {
    // Stats
    level: number = 0
    stats: Record<Stat, number> = {
        str: 10,
        dex: 10,
        con: 10,
        int: 10,
        wis: 10,
        cha: 10,
        none: 10,
    }
    statMax: Record<Stat, number> = {
        str: DEFAULT_STAT_MAX,
        dex: DEFAULT_STAT_MAX,
        con: DEFAULT_STAT_MAX,
        int: DEFAULT_STAT_MAX,
        wis: DEFAULT_STAT_MAX,
        cha: DEFAULT_STAT_MAX,
        none: DEFAULT_STAT_MAX,
    }

    events: EventLoop<CharacterEventName, CharacterEventMapping> =
        new EventLoop()
    effects: Set<string> = new Set()
    masteries: Set<WeaponMastery> = new Set()
    classLevels: Map<Class, number> = new Map()
    feats: Array<Feat> = []
    minions: Set<Character> = new Set()

    spells: Spellcasting = new Spellcasting({
        character: this,
    })

    bonus: Resource = new Resource({
        name: "Bonus",
        character: this,
        initialMax: 1,
    })
    // TODO: Add other class resources

    // TODO: Handle actions better
    actions: number = 1

    addFeat<T extends CharacterEvent>(feat: Feat): void {
        this.feats.push(feat)
        feat.coreApply(this)
    }

    stat(stat: Stat): number {
        return this.stats[stat]
    }

    mod(stat: Stat): number {
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

    dc(stat: Stat): number {
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

    addEffect(effect: string): void {
        this.effects.add(effect)
    }

    removeEffect(effect: string): void {
        this.effects.delete(effect)
    }

    getClassLevel(class_: Class): number {
        return this.classLevels.get(class_) ?? 0
    }

    hasClassLevel(class_: Class, level: number): boolean {
        return (this.getClassLevel(class_) ?? 0) >= level
    }

    addClassLevel(class_: Class, level: number): void {
        this.classLevels.set(class_, this.getClassLevel(class_) + level)
    }

    // =============================
    //       LIFECYCLE EVENTS
    // =============================

    turn(target: Target): void {
        this.actions = 1
        this.bonus.reset()
        this.events.emit("begin_turn", { name: "begin_turn", target })
        this.events.emit("before_action", { name: "before_action", target })
        while (this.actions > 0) {
            this.events.emit("action", new ActionEvent({ target }))
            this.actions -= 1
        }
        this.events.emit("after_action", { name: "after_action", target })
        this.events.emit("end_turn", { name: "end_turn", target })
        this.bonus.reset()
        for (const minion of this.minions) {
            minion.turn(target)
        }
    }

    shortRest(): void {
        this.effects = new Set()
        this.events.emit("short_rest", { name: "short_rest" })
    }

    longRest(): void {
        this.shortRest()
        this.events.emit("long_rest", { name: "long_rest" })
    }

    enemyTurn(target: Target): void {
        this.events.emit("enemy_turn", { name: "enemy_turn", target })
    }

    // =============================
    //       WEAPON EVENTS
    // =============================

    weaponAttack(args: {
        target: Target
        weapon: Weapon
        tags?: string[]
    }): void {
        const attack = new WeaponAttack({
            weapon: args.weapon,
            tags: args.tags,
        })
        this.attack({ target: args.target, attack })
    }

    attack(args: { target: Target; attack: Attack }): void {
        const { target, attack } = args
        const attackData = new AttackEvent({ target, attack })
        this.events.emit("before_attack", { name: "before_attack" })
        const toHit = attack.toHit(this)
        const rollResult = this.attackRoll(attackData, toHit)
        const roll = rollResult.roll()
        const minCrit = rollResult.minCrit
            ? rollResult.minCrit
            : attack.minCrit()
        const crit = roll >= minCrit
        const rollTotal = roll + toHit + rollResult.situationalBonus
        const hit = rollTotal >= target.ac
        const attackResult = new AttackResultEvent({
            attack: attackData,
            hit,
            crit,
            roll,
        })
        args.attack.attackResult(attackResult, this)
        this.events.emit("attack_result", attackResult)
        for (const damage of attackResult.damageRolls) {
            if (crit) {
                damage.dice = damage.dice.concat(damage.dice)
            }
            this.doDamage({ target, damage, attack: attackData, multiplier: 1 })
        }
    }

    attackRoll(attackData: AttackEvent, toHit: number): AttackRollEvent {
        const { target, attack } = attackData
        const data = new AttackRollEvent({ attack: attackData, toHit })
        // TODO: Stunned and semistunned
        if (target.prone) {
            if (attack.isRanged()) {
                data.disadv = true
            } else {
                data.adv = true
            }
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
        target.addDamage(Math.floor(damage.total() * multiplier))
    }
}

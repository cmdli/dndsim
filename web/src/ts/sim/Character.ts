import {
    CharacterEvent,
    CharacterEventData,
    CharacterEventMapping,
} from "./CharacterEvent"
import { Feat } from "./Feat"
import { EventLoop } from "./EventLoop"
import { Class, Stat, WeaponMastery } from "./types"
import { Resource } from "./Resource"
import { Target } from "./Target"

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
    }
    statMax: Record<Stat, number> = {
        str: DEFAULT_STAT_MAX,
        dex: DEFAULT_STAT_MAX,
        con: DEFAULT_STAT_MAX,
        int: DEFAULT_STAT_MAX,
        wis: DEFAULT_STAT_MAX,
        cha: DEFAULT_STAT_MAX,
    }

    events: EventLoop<CharacterEvent, CharacterEventMapping> = new EventLoop()
    effects: Set<string> = new Set()
    masteries: Set<WeaponMastery> = new Set()
    classLevels: Map<Class, number> = new Map()
    feats: Array<Feat<CharacterEvent>> = []
    minions: Set<Character> = new Set()

    bonus: Resource = new Resource("Bonus", this.events, 1)
    // TODO: Add other class resources

    // TODO: Handle actions better
    actions: number = 1

    addFeat<T extends CharacterEvent>(feat: Feat<T>): void {
        this.feats.push(feat)
        feat.apply(this)
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
        this.events.emit("begin_turn", { type: "begin_turn", target })
        this.events.emit("before_action", { type: "before_action", target })
        while (this.actions > 0) {
            this.events.emit("action", { type: "action", target })
            this.actions -= 1
        }
        this.events.emit("after_action", { type: "after_action", target })
        this.events.emit("end_turn", { type: "end_turn", target })
        this.bonus.reset()
        for (const minion of this.minions) {
            minion.turn(target)
        }
    }

    shortRest(): void {
        this.effects = new Set()
        this.events.emit("short_rest", { type: "short_rest" })
    }

    longRest(): void {
        this.shortRest()
        this.events.emit("long_rest", { type: "long_rest" })
    }

    enemyTurn(target: Target): void {
        this.events.emit("enemy_turn", { type: "enemy_turn", target })
    }
}

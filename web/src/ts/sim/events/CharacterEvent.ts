import { Target } from "../Target"
import { ActionEvent } from "./ActionEvent"
import { AttackEvent } from "./AttackEvent"
import { AttackResultEvent } from "./AttackResultEvent"
import { AttackRollEvent } from "./AttackRollEvent"
import { DamageRollEvent } from "./DamageRollEvent"

export type CharacterEventName =
    | "begin_turn"
    | "before_action"
    | "action"
    | "after_action"
    | "before_attack"
    | "attack"
    | "attack_roll"
    | "attack_result"
    | "end_turn"
    | "enemy_turn"
    | "short_rest"
    | "long_rest"
    | "weapon_roll"
    | "cast_spell"
    | "damage_roll"

export abstract class CharacterEvent {
    abstract readonly name: CharacterEventName
}

export type BeginTurnEvent = {
    name: "begin_turn"
    target: Target
}

export type BeforeActionEvent = {
    name: "before_action"
    target: Target
}

export type AfterActionEvent = {
    name: "after_action"
    target: Target
}

export type BeforeAttackEvent = {
    name: "before_attack"
}

export type EndTurnEvent = {
    name: "end_turn"
    target: Target
}

export type EnemyTurnEvent = {
    name: "enemy_turn"
    target: Target
}

export type ShortRestEvent = {
    name: "short_rest"
}

export type LongRestEvent = {
    name: "long_rest"
}

export type WeaponRollEvent = {
    name: "weapon_roll"
}

export type CastSpellEvent = {
    name: "cast_spell"
}

export type CharacterEventData =
    | BeginTurnEvent
    | BeforeActionEvent
    | ActionEvent
    | AfterActionEvent
    | BeforeAttackEvent
    | AttackEvent
    | AttackRollEvent
    | AttackResultEvent
    | EndTurnEvent
    | EnemyTurnEvent
    | ShortRestEvent
    | LongRestEvent
    | WeaponRollEvent
    | CastSpellEvent
    | DamageRollEvent

export type CharacterEventMapping = {
    begin_turn: BeginTurnEvent
    before_action: BeforeActionEvent
    action: ActionEvent
    after_action: AfterActionEvent
    before_attack: BeforeAttackEvent
    attack: AttackEvent
    attack_roll: AttackRollEvent
    attack_result: AttackResultEvent
    end_turn: EndTurnEvent
    enemy_turn: EnemyTurnEvent
    short_rest: ShortRestEvent
    long_rest: LongRestEvent
    weapon_roll: WeaponRollEvent
    cast_spell: CastSpellEvent
    damage_roll: DamageRollEvent
}

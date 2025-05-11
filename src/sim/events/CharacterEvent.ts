import { ActionEvent } from "./ActionEvent"
import { AfterActionEvent } from "./AfterActionEvent"
import { AttackEvent } from "./AttackEvent"
import { AttackResultEvent } from "./AttackResultEvent"
import { AttackRollEvent } from "./AttackRollEvent"
import { BeforeActionEvent } from "./BeforeActionEvent"
import { BeforeAttackEvent } from "./BeforeAttackEvent"
import { BeginTurnEvent } from "./BeginTurnEvent"
import { CastSpellEvent } from "./CastSpellEvent"
import { DamageRollEvent } from "./DamageRollEvent"
import { EndTurnEvent } from "./EndTurnEvent"
import { EnemyTurnEvent } from "./EnemyTurnEvent"
import { LongRestEvent } from "./LongRestEvent"
import { ShortRestEvent } from "./ShortRestEvent"
import { WeaponRollEvent } from "./WeaponRollEvent"

export const CharacterEventNames = [
    "begin_turn",
    "before_action",
    "action",
    "after_action",
    "before_attack",
    "attack",
    "attack_roll",
    "attack_result",
    "end_turn",
    "enemy_turn",
    "short_rest",
    "long_rest",
    "weapon_roll",
    "cast_spell",
    "damage_roll",
] as const
export type CharacterEventName = (typeof CharacterEventNames)[number]

export abstract class CharacterEvent {
    abstract readonly name: CharacterEventName
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

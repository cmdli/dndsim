import { Target } from "./Target"

export type CharacterEvent =
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

export type BeginTurnData = {
    type: "begin_turn"
    target: Target
}

export type BeforeActionData = {
    type: "before_action"
    target: Target
}

export type ActionData = {
    type: "action"
    target: Target
}

export type AfterActionData = {
    type: "after_action"
    target: Target
}

export type BeforeAttackData = {
    type: "before_attack"
}

export type AttackData = {
    type: "attack"
}

export type AttackRollData = {
    type: "attack_roll"
}

export type AttackResultData = {
    type: "attack_result"
}

export type EndTurnData = {
    type: "end_turn"
    target: Target
}

export type EnemyTurnData = {
    type: "enemy_turn"
    target: Target
}

export type ShortRestData = {
    type: "short_rest"
}

export type LongRestData = {
    type: "long_rest"
}

export type WeaponRollData = {
    type: "weapon_roll"
}

export type CastSpellData = {
    type: "cast_spell"
}

export type DamageRollData = {
    type: "damage_roll"
}

export type CharacterEventData =
    | BeginTurnData
    | BeforeActionData
    | ActionData
    | AfterActionData
    | BeforeAttackData
    | AttackData
    | AttackRollData
    | AttackResultData
    | EndTurnData
    | EnemyTurnData
    | ShortRestData
    | LongRestData
    | WeaponRollData
    | CastSpellData
    | DamageRollData

export type CharacterEventMapping = {
    begin_turn: BeginTurnData
    before_action: BeforeActionData
    action: ActionData
    after_action: AfterActionData
    before_attack: BeforeAttackData
    attack: AttackData
    attack_roll: AttackRollData
    attack_result: AttackResultData
    end_turn: EndTurnData
    enemy_turn: EnemyTurnData
    short_rest: ShortRestData
    long_rest: LongRestData
    weapon_roll: WeaponRollData
    cast_spell: CastSpellData
    damage_roll: DamageRollData
}

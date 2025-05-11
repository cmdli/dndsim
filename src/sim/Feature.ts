import { Character } from "./Character"
import {
    CharacterEventName,
    CharacterEventNames,
} from "./events/CharacterEvent"

const EVENT_LISTENER_NAME: Record<CharacterEventName, string> = {
    begin_turn: "beginTurn",
    before_action: "beforeAction",
    action: "action",
    after_action: "afterAction",
    before_attack: "beforeAttack",
    attack: "attack",
    attack_roll: "attackRoll",
    attack_result: "attackResult",
    end_turn: "endTurn",
    enemy_turn: "enemyTurn",
    short_rest: "shortRest",
    long_rest: "longRest",
    weapon_roll: "weaponRoll",
    cast_spell: "castSpell",
    damage_roll: "damageRoll",
}

export abstract class Feature {
    // Allow feats to expect the character to be set in their implementations
    // of apply
    declare character: Character

    internalApply(character: Character): void {
        this.character = character
        this.addEventListeners(character)
        this.apply(character)
    }

    addEventListeners(character: Character): void {
        // DISCLAIMER: This isn't very well typed, so be careful about modifying it
        for (const event of CharacterEventNames) {
            const thisClass = this as any
            const listenerName = EVENT_LISTENER_NAME[event]
            const listener = thisClass[listenerName]
            if (typeof listener === "function") {
                const typedListener = listener as Function
                character.events.on(event, (event) => {
                    typedListener.call(thisClass, event)
                })
            }
        }
    }

    apply(character: Character): void {}
}

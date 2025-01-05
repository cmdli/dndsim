# How It Works

## Events

At the heart of the simulator is the concept of an event. Events are particular actions taken by the simulator, such as attacks, spells, damage rolls, turns, etc. Each event is emitted to the event loop, which then broadcasts out that event to all listeners. Listeners can then modify the character or the target, or trigger other events, or event modify the parameters of the event. This allows for features to be added that can modify character behavior in a modular fashion.

## Feats

Features (or feats) are the most common type of listener to events. They are pieces of code that can be added to a character that listen for events on that character and then trigger behavior. For example, a feat may add extra damage to a character's attack, but only if that attack is with a weapon.

Most features of a class are added as feats so that they can be applied modularly depending on how many levels the character has in that class. Feats can also be added or removed for class features like Agonizing Blast depending on the invocations taken.

## Character Turns

Character turns are broken up into several standard events:

- `begin_turn`
- `before_action`
- `action`
- `after_action`
- `end_turn`

Feats can be added to use features or resources during these events. The most important event is the `action` event, which is where the majority of the character's behavior will be.

Bonus actions are tracked separately with the `character.use_bonus()` function, which will attempt to use the bonus action and return true or false if the bonus action was used up.

### Minions

Minions are extra characters that the main character can add. They take their turns after the main character. Some examples are the Ranger's beast companion or the Summon X spells.

## Limitations/Inaccuracies

- The target has the same saving throw bonus for all saves
- Damage resistances/immunities are ignored
- Target AC follows the DMG recommended AC, which is not representative of actual monsters
- Spacing and positioning is ignored
- Target's take no actions during their turn other than standing up from prone
- Some features have assumptions (such as the Barbarian's Retaliation assuming it is triggered every enemy turn)
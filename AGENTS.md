# AGENTS.md - Agent Overview

This library serves as simulation code for D&D 2024 edition, allowing users of this library to measure the amount of damage a particular character build can do.

## Code Overview

`python` contains legacy python code and can mostly be ignored unless explicitly asked to make changes to it.
`src` contains the main Typescript code for this package.
`script` is a directory for developer scripts for testing and local usage.
`src/index.ts` is the entrypoint for the library to export all used members.
`src/classes` contains the class-specific code and Features for simulating a particular class.
`src/spells` contains all the spell implementations but not the spell framework code.
`src/weapons` contains all the weapon implementations but not the weapon framework code.
`src/feats` contains all the feats (features) that classes might use. These are mainly feats that can be optionally taken outside of normal class features.
`src/operations` contains the implementation of various operations that a character can take on its turn using the custom turn code.
`src/sim` contains the core simulation framework code.
`src/sim/Simulation.ts` is the entrypoint for running a simulation.
`src/sim/Character.ts` contains the code for tracking a Character with their features, turn, actions, and other effects.
`src/sim/Attack.ts` contains the code for running an attack by a character onto a target. These attacks can be weapon attacks or spell attacks.
`src/sim/Feature.ts` is the core framework code for Features.
`src/sim/Weapon.ts` contains the framework code for weapons.
`src/sim/Effect.ts` contains the framework code for effects that apply to the character.
`src/sim/spells` contains the spell framework code.
`src/sim/actions` contains the framework code for the actions a character can choose to take on its turn.
`src/sim/events` contains all the events that are emitted by the framework that features can respond to.
`src/sim/resources` contains the code to track character resources.

## High Level Concepts

### Character

A character represents a D&D character. This character can take actions, cast spells, attack the target, etc. The Character object is where all the character's resources and actions are tracked.

### Feature

A Feature is a bit of code and functionality that can be applied to a Character modularly. A Character can have many features which will modify the character, such as increasing stats or adding responses to certain events. The Feature code is very simple, just being a method that can be called to apply to a particular character.

All Features are applied at the start before any simulation begins.

### Target

The Target is the singular target for many spells and attacks. The Target tracks the amount of damage dealt to it, as well as has its own turns and event loops. In concept, this Target would be something like a Goblin or Ogre, but here it is abstracted and has infinite health.

The stats of the Target are based on the Character level, and go up as the Character becomes higher level.

### Weapon

A weapon is simply a physical weapon in the simulation, like a dagger or shortsword or club. Each weapon has certain stats like amount of damage or what Character stat it uses to calculate the to-hit modifier.

Each weapon also has a weapon mastery, which is an optional property that may be enabled if the character has the corresponding weapon mastery. These weapon masteries do additional effects to the target. Some effects, such as Sap, are ignored because they do not affect the damage calculation of the simulation.

### Effect

An Effect is a temporary effect that can be placed onto a character or a target. These effects can call custom code in order to apply things like extra damage, conditions, or trigger other abilities. Each Effect can add event listeners on the target, and the Character object tracks when effects are started and ended.

### Turn Structure

The simulation goes as follows:

1. The Character and Target take a long rest (which includes a short rest).
2. A fight happens:
    1. One round happens:
        1. The Character has a turn.
        2. The Target has a turn.
    2. These rounds continue until the round limit is reached.
    3. The character and target take a short rest.
3. Another fight happens again and again until the fight limit is reached.
4. The total damage on the Target is calculated and usually divided by the number of rounds to get the Damage per Round (DPR) calculation.

### Attack

An attack is made by a character onto the target. To do so, you roll a d20 die and add the to-hit modifier for the character for that attack/weapon. Then you compare it to the AC of the target, and the number is greater then it is successful, causing damage and sometimes other effects.

Spells can sometimes make attacks as well. These use the spell attack modifier for the character.

### Spells

A Spell is a magical effect that a character can cause, sometimes using resources call spell slots. A spell slot is a limited resource used to fuel spells and oftentimes refreshes on a long rest. These spells can do many different things, from dealing damage to conjuring helpers to buffing the Character.

#### Spell Summons

Spells can occasionally summon allies, which are full Characters with oftentimes limited sets of Features. These characters take their turn right after the owning character (who cast the spell) takes their turn.

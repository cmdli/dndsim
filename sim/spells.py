from typing import List, Optional

import sim.target
import sim.character
import sim.events
import sim.attack
import util.taggable


class Spell(util.taggable.Taggable):
    def __init__(
        self, name: str, slot: int, concentration: bool = False, duration: int = 0
    ):
        self.name = name
        self.slot = slot
        self.concentration = concentration
        self.duration = duration

    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        self.character = character

    def end(self, character: "sim.character.Character"):
        pass


class TargetedSpell(Spell):
    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        super().cast(character, target)
        if not target:
            return
        self.cast_target(character, target)

    def cast_target(
        self, character: "sim.character.Character", target: "sim.target.Target"
    ):
        pass


class ConcentrationSpell(Spell):
    def __init__(self, name: str, slot: int, **kwargs):
        super().__init__(name, slot, concentration=True, **kwargs)

    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        super().cast(character, target)
        character.add_effect(self.name)

    def end(self, character: "sim.character.Character"):
        super().end(character)
        character.remove_effect(self.name)


class BasicSaveSpell(Spell):
    def __init__(self, name: str, slot: int, dice: List[int], flat_dmg: int = 0):
        super().__init__(name, slot)
        self.dice = dice
        self.flat_dmg = flat_dmg

    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        if not target:
            return
        super().cast(character, target)
        saved = target.save(character.spells.dc())
        character.do_damage(
            target,
            damage=sim.attack.DamageRoll(
                source=self.name,
                dice=self.dice,
                flat_dmg=self.flat_dmg,
            ),
            spell=self,
            multiplier=0.5 if saved else 1,
        )

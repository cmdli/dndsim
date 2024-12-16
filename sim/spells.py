from typing import List, Tuple, Optional
import math
from enum import Enum

from util.log import log
from util.util import spell_slots, highest_spell_slot, lowest_spell_slot

import sim.spells
import sim.target
import sim.character
import sim.target
import sim.attack
import sim.events
import sim.event_loop

import util.taggable


class Spellcaster(Enum):
    FULL = 0
    HALF = 1
    THIRD = 2
    NONE = 3


def spellcaster_level(levels: List[Tuple[Spellcaster, int]]):
    total = 0
    for type, level in levels:
        if type is Spellcaster.FULL:
            total += level
        elif type is Spellcaster.HALF:
            total += math.ceil(float(level) / 2)
        elif type is Spellcaster.THIRD:
            total += math.ceil(float(level) / 3)
    return total


class Spellcasting(sim.event_loop.Listener):
    def __init__(
        self,
        character: "sim.character.Character",
        mod: "sim.Stat",
        spellcaster_levels: List[Tuple[Spellcaster, int]],
    ) -> None:
        self.character = character
        self.mod = mod
        self.spellcaster_level = spellcaster_level(spellcaster_levels)
        self.concentration: Optional["sim.spells.Spell"] = None
        self.spells: List["sim.spells.Spell"] = []
        self.slots = spell_slots(self.spellcaster_level)
        self.to_hit_bonus = 0
        self.character.events.add(self, ["short_rest"])

    def reset(self):
        self.slots = spell_slots(self.spellcaster_level)
        self.short_rest()

    def short_rest(self):
        self.set_concentration(None)
        for spell in self.spells:
            spell.end(self.character)

    def dc(self):
        return 8 + self.character.mod(self.mod) + self.character.prof

    def highest_slot(self, max: int = 9) -> int:
        return highest_spell_slot(self.slots, max=max)

    def lowest_slot(self, min: int = 1) -> int:
        return lowest_spell_slot(self.slots, min=min)

    def cast(
        self,
        spell: "sim.spells.Spell",
        target: Optional["sim.target.Target"] = None,
    ):
        log.record(f"Cast ({spell.name})", 1)
        if spell.slot > 0:
            self.slots[spell.slot] -= 1
        if spell.concentration:
            self.set_concentration(spell)
        spell.cast(self.character, target)
        if spell.duration > 0 or spell.concentration:
            self.spells.append(spell)

    def end_spell(self, spell: "sim.spells.Spell"):
        self.spells.remove(spell)
        spell.end(self.character)

    def set_concentration(self, spell: "sim.spells.Spell"):
        if self.concentration:
            self.spells.remove(self.concentration)
            self.concentration.end(self.character)
        self.concentration = spell

    def concentrating_on(self, name: str) -> bool:
        return self.concentration is not None and self.concentration.name is name

    def is_concentrating(self) -> bool:
        return self.concentration is not None

    def cantrip_dice(self):
        if self.character.level >= 17:
            return 4
        elif self.character.level >= 11:
            return 3
        elif self.character.level >= 5:
            return 2
        return 1

    def to_hit(self):
        return self.character.mod(self.mod) + self.character.prof + self.to_hit_bonus


class School(Enum):
    Abjuration = 1
    Conjuration = 2
    Divination = 3
    Enchantment = 4
    Evocation = 5
    Illusion = 6
    Necromancy = 7
    Transmutation = 8


class Spell(util.taggable.Taggable):
    def __init__(
        self,
        name: str,
        slot: int,
        concentration: bool = False,
        duration: int = 0,
        school: Optional[School] = None,
    ):
        self.name = name
        self.slot = slot
        self.concentration = concentration
        self.duration = duration
        self.school = school

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
    def __init__(
        self, name: str, slot: int, dice: List[int], flat_dmg: int = 0, **kwargs
    ):
        super().__init__(name, slot, **kwargs)
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

from util.util import spell_slots, highest_spell_slot, lowest_spell_slot
from enum import Enum
import sim.spells
import sim.target
import sim.character
from typing import List, Tuple
import math
from util.log import log


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


class Spellcasting:
    def __init__(
        self,
        character: "sim.character.Character",
        mod: str,
        spellcaster_levels: List[Tuple[Spellcaster, int]],
    ) -> None:
        self.character = character
        self.mod = mod
        self.spellcaster_level = spellcaster_level(spellcaster_levels)
        self.concentration: "sim.spells.Spell" = None
        self.spells: List["sim.spells.Spell"] = []

    def reset(self):
        self.slots = spell_slots(self.spellcaster_level)
        self.set_concentration(None)
        for spell in self.spells:
            spell.end(self.character)

    def dc(self):
        return 8 + self.character.mod(self.mod) + self.character.prof

    def highest_slot(self, max: int = 9) -> int:
        return highest_spell_slot(self.slots, max=max)

    def lowest_slot(self, min: int = 1) -> int:
        return lowest_spell_slot(self.slots, min=min)

    def cast(self, spell: "sim.spells.Spell", target: "sim.target.Target" = None):
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

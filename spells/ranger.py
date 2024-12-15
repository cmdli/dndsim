from typing import Optional

from sim.character import Character
import sim.spellcasting
from sim.spellcasting import School

import sim.target


class HuntersMark(sim.spellcasting.ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot, school=School.Divination)
        self.target: Optional["sim.target.Target"] = None

    def cast(self, character: Character, target: Optional["sim.target.Target"] = None):
        super().cast(character, target)
        if target:
            target.add_tag("HuntersMark")
            self.target = target

    def end(self, character: Character):
        super().end(character)
        if self.target:
            self.target.remove_tag("HuntersMark")

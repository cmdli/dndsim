from typing import Optional

from sim.spells import School

import sim.spells
import sim.target


class HuntersMark(sim.spells.ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot, school=School.Divination)
        self.target: Optional["sim.target.Target"] = None

    def cast(self, character, target: Optional["sim.target.Target"] = None):
        super().cast(character, target)
        if target:
            target.add_tag("HuntersMark")
            self.target = target

    def end(self, character):
        super().end(character)
        if self.target:
            self.target.remove_tag("HuntersMark")

from typing import Optional

from sim.spells import School

import sim.spells
import sim.target
import sim.events


class HuntersMark(sim.spells.ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot, school=School.Divination)
        self.target: Optional["sim.target.Target"] = None

    def cast(self, character, target: Optional["sim.target.Target"] = None):
        super().cast(character, target)
        character.events.add(self, "attack_result")
        if target:
            target.add_tag("HuntersMark")
            self.target = target

    def attack_result(self, args: "sim.events.AttackResultArgs"):
        if args.hits() and args.attack.target.has_tag("HuntersMark"):
            args.add_damage(source="HuntersMark", dice=[6])

    def end(self, character):
        super().end(character)
        character.events.remove(self)
        if self.target:
            self.target.remove_tag("HuntersMark")

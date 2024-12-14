from sim.character import Character
import sim.spells
from sim.spells import School
from sim.target import Target


class HuntersMark(sim.spells.ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot, school=School.Divination)
        self.target = None

    def cast(self, character: Character, target: Target | None = None):
        super().cast(character, target)
        target.add_tag("HuntersMark")
        self.target = target

    def end(self, character: Character):
        super().end(character)
        if self.target:
            self.target.remove_tag("HuntersMark")

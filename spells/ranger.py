import sim.spells
from sim.spells import School


class HuntersMark(sim.spells.ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot, school=School.Divination)

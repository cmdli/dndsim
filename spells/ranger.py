import sim.spells


class HuntersMark(sim.spells.ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot)

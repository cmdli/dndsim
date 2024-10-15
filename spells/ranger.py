from sim.spells import ConcentrationSpell


class HuntersMark(ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot)

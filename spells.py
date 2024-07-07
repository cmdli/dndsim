class Spell:
    def __init__(self, name: str, slot: int, concentration: bool = False):
        self.name = name
        self.slot = slot
        self.concentration = concentration

    def begin(self):
        pass

    def end(self):
        pass


class HuntersMark(Spell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot, concentration=True)


class DivineSmite(Spell):
    def __init__(self, slot: int):
        super().__init__("DivineSmite", slot)

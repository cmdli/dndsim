from sim.spells import Spell, ConcentrationSpell
import sim.character
import sim.target
from util.util import roll_dice


class DivineSmite(Spell):
    def __init__(self, slot: int, crit: bool):
        super().__init__("DivineSmite", slot=slot)
        self.crit = crit

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        num_dice = 1 + self.slot
        if self.crit:
            num_dice *= 2
        target.damage_source("DivineSmite", roll_dice(num_dice, 8))


class DivineFavor(ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("DivineFavor", slot)


class HolyWeapon(ConcentrationSpell):
    def __init__(self, slot: int, **kwargs):
        super().__init__("HolyWeapon", slot=slot, **kwargs)

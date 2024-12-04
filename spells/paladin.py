from util.util import roll_dice

from sim.spells import School
import sim.character
import sim.target
import sim.spells


class DivineSmite(sim.spells.TargetedSpell):
    def __init__(self, slot: int, crit: bool):
        super().__init__("DivineSmite", slot=slot, school=School.Evocation)
        self.crit = crit

    def cast_target(
        self,
        character: "sim.character.Character",
        target: "sim.target.Target",
    ):
        num_dice = 1 + self.slot
        if self.crit:
            num_dice *= 2
        target.damage_source("DivineSmite", roll_dice(num_dice, 8))


class DivineFavor(sim.spells.ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("DivineFavor", slot, school=School.Transmutation)


class HolyWeapon(sim.spells.ConcentrationSpell):
    def __init__(self, slot: int, **kwargs):
        super().__init__("HolyWeapon", slot=slot, school=School.Evocation, **kwargs)

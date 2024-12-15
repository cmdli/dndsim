from util.util import roll_dice

from sim.spells import School
import sim.character
import sim.target
import sim.spells
import sim.weapons
import sim.events


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
    def __init__(self, slot: int, weapon: "sim.weapons.Weapon", **kwargs):
        super().__init__("HolyWeapon", slot=slot, school=School.Evocation, **kwargs)
        self.weapon = weapon

    def cast(self, character, target=None):
        super().cast(character, target)
        character.events.add(self, "attack_result")

    def end(self, character):
        super().end(character)
        character.events.remove(self)

    def attack_result(self, args: "sim.events.AttackResultArgs"):
        if args.hits() and args.attack.weapon is self.weapon:
            args.add_damage(source=self.name, dice=[8, 8])

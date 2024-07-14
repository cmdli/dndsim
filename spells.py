from target import Target
from util import roll_dice
from weapons import Weapon
from enum import Enum


class Spellcaster(Enum):
    FULL = 0
    HALF = 1
    NONE = 2


class Spell:
    def __init__(
        self,
        name: str,
        slot: int,
        concentration: bool = False,
    ):
        self.name = name
        self.slot = slot
        self.concentration = concentration

    def cast(self, character, target: Target):
        pass

    def end(self):
        pass


class ConcentrationSpell(Spell):
    def __init__(self, name: str, slot: int, **kwargs):
        super().__init__(name, slot, concentration=True, **kwargs)

    def cast(self, character, target: Target):
        character.add_effect(self.name)

    def end(self, character):
        self.character.add_effect(self.name)


class HuntersMark(ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot)


class DivineSmite(Spell):
    def __init__(self, slot: int, crit: bool):
        super().__init__("DivineSmite", slot=slot)
        self.crit = crit

    def cast(self, character, target: Target):
        num_dice = 1 + self.slot
        if self.crit:
            num_dice *= 2
        target.damage_source("DivineSmite", roll_dice(num_dice, 8))


class DivineFavor(ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("DivineFavor", slot)


class Fireball(Spell):
    def __init__(self, slot: int):
        super().__init__("Fireball", slot)

    def cast(self, character, target: Target):
        dmg = roll_dice(5 + self.slot, 6)
        if target.save(character.spell_dc()):
            dmg = dmg // 2
        target.damage_source("Fireball", dmg)


class TrueStrike(Spell):
    def __init__(self, slot: int, weapon: Weapon, **kwargs):
        super().__init__("TrueStrike", slot)
        self.weapon = weapon

    def cast(self, character, target: Target):
        self.character.attack(target, self.weapon, tags=["truestrike"])

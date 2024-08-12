import sim.target
from util.util import roll_dice, cantrip_dice
from sim.weapons import Weapon
import sim.character


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

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        pass

    def end(self, character: "sim.character.Character"):
        pass


class ConcentrationSpell(Spell):
    def __init__(self, name: str, slot: int, **kwargs):
        super().__init__(name, slot, concentration=True, **kwargs)

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        character.add_effect(self.name)

    def end(self, character: "sim.character.Character"):
        character.remove_effect(self.name)


class HuntersMark(ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot)


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


class Fireball(Spell):
    def __init__(self, slot: int):
        super().__init__("Fireball", slot)

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        dmg = roll_dice(5 + self.slot, 6)
        if target.save(character.spells.dc()):
            dmg = dmg // 2
        target.damage_source("Fireball", dmg)


class TrueStrike(Spell):
    def __init__(self, weapon: Weapon, **kwargs):
        super().__init__("TrueStrike", 0)
        self.weapon = weapon

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        character.attack(target, self.weapon, tags=["truestrike"])


class HolyWeapon(ConcentrationSpell):
    def __init__(self, slot: int, **kwargs):
        super().__init__("HolyWeapon", slot=slot, **kwargs)


class EldritchBlastBolt(Weapon):
    def __init__(self, **kwargs):
        super().__init__("EldritchBlastBolt", num_dice=1, die=10, mod="none")


class EldritchBlast(Spell):
    def __init__(self, character_level: int, **kwargs):
        super().__init__("EldritchBlast", 0, **kwargs)
        self.character_level = character_level
        self.weapon = EldritchBlastBolt()
        self.num_bolts = cantrip_dice(character_level)

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        for _ in range(self.num_bolts):
            character.attack(target, self.weapon)

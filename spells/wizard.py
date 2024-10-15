from typing import List
from sim.spells import Spell, BasicSaveSpell
from sim.target import Target
from sim.weapons import Weapon
import sim.character

from util.util import roll_dice


class MeteorSwarm(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("MeteorSwarm", slot)
        assert slot == 9

    def damage(self):
        return roll_dice(40, 6)


class FingerOfDeath(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("FingerOfDeath", slot)
        assert slot >= 7

    def damage(self):
        return roll_dice(7, 8) + 30


class ChainLightning(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("ChainLightning", slot)

    def damage(self):
        return roll_dice(10, 8)


class Blight(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("Blight", slot)

    def damage(self):
        return roll_dice(4 + self.slot, 8)


class Fireball(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("Fireball", slot)

    def damage(self):
        return roll_dice(5 + self.slot, 6)


class ScorchingRayWeapon(Weapon):
    def __init__(self, character: "sim.character.Character", spell: Spell):
        super().__init__(
            name="ScorchingRay",
            num_dice=2,
            die=6,
            damage_type="fire",
            override_mod=character.spells.mod,
            spell=spell,
        )


class ScorchingRay(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("ScorchingRay", slot)

    def cast(self, character: "sim.character.Character", target: Target):
        super().cast(character, target)
        weapon = ScorchingRayWeapon(character, self)
        for _ in range(1 + self.slot):
            character.attack(target, weapon, tags=["spell"])


class MagicMissile(Spell):
    def __init__(self, slot: int):
        super().__init__("MagicMissile", slot)

    def cast(self, character: "sim.character.Character", target: Target):
        super().cast(character, target)
        target.damage_source(self.name, roll_dice(2 + self.slot, 4) + 2 + self.slot)


class FireboltWeapon(Weapon):
    def __init__(self, character: "sim.character.Character", spell: Spell):
        super().__init__(
            "Firebolt",
            num_dice=character.spells.cantrip_dice(),
            die=10,
            damage_type="fire",
            override_mod=character.spells.mod,
            spell=spell,
        )


class Firebolt(Spell):
    def __init__(self):
        super().__init__("Firebolt", slot=0)

    def cast(self, character: "sim.character.Character", target: Target):
        super().cast(character, target)
        weapon = FireboltWeapon(character, self)
        character.attack(target, weapon, tags=["spell"])


class TrueStrike(Spell):
    def __init__(self, weapon: "sim.weapons.Weapon", **kwargs):
        super().__init__("TrueStrike", 0)
        self.weapon = weapon

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        character.attack(target, self.weapon, tags=["truestrike"])

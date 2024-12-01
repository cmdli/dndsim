from typing import List, Optional
import sim.attack
from sim.spells import Spell, BasicSaveSpell
from sim.target import Target
from sim.weapons import Weapon
import sim.character
import sim.events
import sim.spells

from util.util import roll_dice


class MeteorSwarm(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("MeteorSwarm", slot)
        assert slot == 9

    def dice(self) -> List[int]:
        return 40 * [6]


class FingerOfDeath(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("FingerOfDeath", slot)
        assert slot >= 7

    def dice(self) -> List[int]:
        return 7 * [8]

    def flat_damage(self) -> int:
        return 30


class ChainLightning(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("ChainLightning", slot)

    def dice(self) -> List[int]:
        return 10 * [8]


class Blight(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("Blight", slot)

    def dice(self) -> List[int]:
        num_dice = 4 + self.slot
        return num_dice * [8]


class Fireball(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("Fireball", slot)

    def dice(self):
        num_dice = 5 + self.slot
        return num_dice * [6]


class ScorchingRay(sim.spells.TargetedSpell):
    def __init__(self, slot: int):
        super().__init__("ScorchingRay", slot)

    def cast_target(self, character: "sim.character.Character", target: Target):
        for _ in range(1 + self.slot):
            character.spell_attack(
                target=target,
                spell=self,
                damage=sim.attack.DamageRoll(dice=[6, 6]),
                is_ranged=True,
            )


class MagicMissile(sim.spells.TargetedSpell):
    def __init__(self, slot: int):
        super().__init__("MagicMissile", slot)

    def cast_target(self, character: "sim.character.Character", target: Target):
        num_dice = 2 + self.slot
        character.do_damage(
            target,
            source=self.name,
            dice=num_dice * [4],
            flat_dmg=2 + self.slot,
            spell=self,
        )


class Firebolt(sim.spells.TargetedSpell):
    def __init__(self):
        super().__init__("Firebolt", slot=0)

    def cast_target(self, character: "sim.character.Character", target: Target):
        character.spell_attack(
            target=target,
            spell=self,
            damage=sim.attack.DamageRoll(
                num_dice=character.spells.cantrip_dice(), die=10
            ),
        )


class TrueStrike(Spell):
    def __init__(self, weapon: "sim.weapons.Weapon", **kwargs):
        super().__init__("TrueStrike", 0)
        self.weapon = weapon

    def cast(
        self, character: "sim.character.Character", target: Optional[Target] = None
    ):
        if not target:
            return
        character.weapon_attack(target, self.weapon, tags=["truestrike"])

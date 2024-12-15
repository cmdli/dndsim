from typing import List, Optional

from sim.spellcasting import Spell, BasicSaveSpell, School

import sim.attack
import sim.target
import sim.character
import sim.events
import sim.spellcasting
import sim.weapons


class MeteorSwarm(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("MeteorSwarm", slot, dice=40 * [6], school=School.Evocation)
        assert slot == 9


class FingerOfDeath(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__(
            "FingerOfDeath", slot, dice=7 * [8], flat_dmg=30, school=School.Necromancy
        )
        assert slot >= 7


class ChainLightning(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("ChainLightning", slot, dice=10 * [8], school=School.Evocation)
        assert slot >= 6


class Blight(sim.spellcasting.BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__(
            "Blight", slot, dice=(4 + slot) * [8], school=School.Necromancy
        )


class Fireball(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__(
            "Fireball", slot, dice=(5 + slot) * [6], school=School.Evocation
        )


class ScorchingRay(sim.spellcasting.TargetedSpell):
    def __init__(self, slot: int):
        super().__init__("ScorchingRay", slot, school=School.Evocation)

    def cast_target(
        self, character: "sim.character.Character", target: "sim.target.Target"
    ):
        for _ in range(1 + self.slot):
            character.spell_attack(
                target=target,
                spell=self,
                damage=sim.attack.DamageRoll(source=self.name, dice=[6, 6]),
                is_ranged=True,
            )


class MagicMissile(sim.spellcasting.TargetedSpell):
    def __init__(self, slot: int):
        super().__init__("MagicMissile", slot, school=School.Evocation)

    def cast_target(
        self, character: "sim.character.Character", target: "sim.target.Target"
    ):
        num_dice = 2 + self.slot
        character.do_damage(
            target,
            damage=sim.attack.DamageRoll(
                source=self.name,
                num_dice=num_dice,
                die=4,
                flat_dmg=2 + self.slot,
            ),
            spell=self,
        )


class Firebolt(sim.spellcasting.TargetedSpell):
    def __init__(self):
        super().__init__("Firebolt", slot=0, school=School.Evocation)

    def cast_target(
        self, character: "sim.character.Character", target: "sim.target.Target"
    ):
        character.spell_attack(
            target=target,
            spell=self,
            damage=sim.attack.DamageRoll(
                source=self.name,
                num_dice=character.spells.cantrip_dice(),
                die=10,
            ),
        )


class TrueStrike(Spell):
    def __init__(self, weapon: "sim.weapons.Weapon", **kwargs):
        super().__init__("TrueStrike", 0, school=School.Divination)
        self.weapon = weapon

    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        if not target:
            return
        character.weapon_attack(target, self.weapon, tags=["truestrike"])

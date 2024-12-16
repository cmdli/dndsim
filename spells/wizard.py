from typing import List, Optional

from sim.spells import Spell, BasicSaveSpell, School

import sim.attack
import sim.target
import sim.character
import sim.events
import sim.spells
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


class Blight(sim.spells.BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__(
            "Blight", slot, dice=(4 + slot) * [8], school=School.Necromancy
        )


class Fireball(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__(
            "Fireball", slot, dice=(5 + slot) * [6], school=School.Evocation
        )


class ScorchingRay(sim.spells.TargetedSpell):
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


class MagicMissile(sim.spells.TargetedSpell):
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


class Firebolt(sim.spells.TargetedSpell):
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


class TrueStrikeAttack:
    def __init__(self, weapon: "sim.weapons.Weapon") -> None:
        self.name = "TrueStrikeAttack"
        self.weapon = weapon

    def to_hit(self, character: "sim.character.Character"):
        return character.spells.to_hit()

    def attack_result(
        self, args: "sim.events.AttackResultArgs", character: "sim.character.Character"
    ):
        self.weapon.attack_result(args, character)
        if args.hits():
            num_dice = character.spells.cantrip_dice() - 1
            if num_dice > 0:
                args.add_damage(source=self.name, dice=num_dice * [6])

    def min_crit(self):
        return 20

    def is_ranged(self):
        return False


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
        character.attack(
            target=target, attack=TrueStrikeAttack(self.weapon), weapon=self.weapon
        )

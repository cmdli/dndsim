import random
from enum import Enum

from util.util import roll_dice
from util.log import log
from sim.target import Target
import sim.weapons
from collections import defaultdict
from typing import Set, List
import sim.spells
import sim.character


class AttackArgs:
    def __init__(
        self,
        character: "sim.character.Character",
        target: Target,
        weapon: sim.weapons.Weapon,
        tags: List[str] = None,
        mod: str = "none",
    ):
        self.character = character
        self.target = target
        self.weapon = weapon
        self.mod = mod
        self.tags = set(tags) if tags is not None else None

    def has_tag(self, tag: str):
        return self.tags is not None and tag in self.tags

    def add_tag(self, tag: str):
        if self.tags is None:
            self.tags = set()
        self.tags.add(tag)

    def remove_tag(self, tag: str):
        if self.tags is not None and tag in self.tags:
            self.tags.remove(tag)


class AttackRollArgs:
    def __init__(self, attack: AttackArgs, to_hit: int):
        self.attack = attack
        self.to_hit = to_hit
        self.adv = False
        self.disadv = False
        self.roll1 = random.randint(1, 20)
        self.roll2 = random.randint(1, 20)
        self.situational_bonus = 0

    def reroll(self):
        self.roll1 = random.randint(1, 20)
        self.roll2 = random.randint(1, 20)

    def roll(self):
        if self.adv == self.disadv:
            log.output(lambda: f"Roll: {self.roll1}")
            return self.roll1
        elif self.adv:
            log.output(lambda: f"Roll ADV: {self.roll1}, {self.roll2}")
            return max(self.roll1, self.roll2)
        else:
            log.output(lambda: f"Roll DIS: {self.roll1}, {self.roll2}")
            return min(self.roll1, self.roll2)

    def hits(self):
        return (
            self.roll() + self.to_hit + self.situational_bonus >= self.attack.target.ac
        )


class AttackResultArgs:
    def __init__(
        self,
        attack: AttackArgs,
        hit: bool = False,
        crit: bool = False,
        roll: int = 0,
    ):
        self._dice = defaultdict(list)
        self._flat_dmg = defaultdict(int)
        self.hit = hit
        self.dmg_multiplier = 1.0
        self.attack = attack
        self.crit = crit
        self.roll = roll

    def add_damage(self, source: str, dice: List[int] = None, damage: int = 0):
        if damage:
            self._flat_dmg[source] += damage
        if dice:
            self._dice[source].extend(dice)

    def add_damage_dice(self, source: str, num: int, size: int):
        self.add_damage(source, dice=[size] * num)

    def add_flat_damage(self, source: str, damage: int):
        self.add_damage(source, damage=damage)

    def damage_sources(self) -> Set[str]:
        return set(self._dice.keys()).union(set(self._flat_dmg.keys()))

    def hits(self) -> bool:
        return self.hit

    def misses(self) -> bool:
        return not self.hit


class EnemySavingThrowArgs:
    def __init__(self) -> None:
        pass


class EnemyDamageArgs:
    def __init__(
        self,
        rolls: List[int],
        flat_damage: int,
        weapon: "sim.weapons.Weapon" = None,
        spell: "sim.spells.Spell" = None,
    ) -> None:
        self.rolls = rolls
        self.flat_damage = flat_damage
        self.weapon = weapon
        self.spell = spell


class WeaponRollArgs:
    def __init__(
        self, weapon: sim.weapons.Weapon, rolls: List[int], crit: bool = False
    ) -> None:
        self.weapon = weapon
        self.rolls = rolls
        self.crit = crit


class CastSpellArgs:
    def __init__(self, spell: "sim.spells.Spell") -> None:
        self.spell = spell


class DamageRollArgs:
    def __init__(
        self,
        target: Target = None,
        dice: List[int] = None,
        flat_dmg: int = 0,
        attack: AttackArgs = None,
        spell: "sim.spells.Spell" = None,
    ) -> None:
        self.target = target
        self.dice = dice or []
        self.flat_dmg = flat_dmg
        self.spell = spell
        self.attack = attack

    def damage_total(self):
        total = self.flat_dmg
        for die in self.dice:
            total += roll_dice(1, die)
        return total

import random
from enum import Enum

from util.log import log
from sim.target import Target
import sim.weapons
from collections import defaultdict
from typing import Set, List
import sim.spells


class AttackArgs:
    def __init__(
        self,
        character,
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
        self._dmg = defaultdict(int)
        self.hit = hit
        self.dmg_multiplier = 1
        self.attack = attack
        self.crit = crit
        self.roll = roll

    def add_damage(self, source: str, dmg: int):
        self._dmg[source] += dmg

    def total_damage(self):
        total = 0
        for key in self._dmg:
            total += self._dmg[key]
        return total

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

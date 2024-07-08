import random

from log import log
from target import Target
from weapons import Weapon
from collections import defaultdict
from typing import List


class AttackArgs:
    def __init__(
        self,
        character,
        target: Target,
        weapon: Weapon,
        tags: List[str] = [],
    ):
        self.character = character
        self.target = target
        self.weapon = weapon
        self.tags = tags

    def has_tag(self, tag: str):
        return tag in self.tags

    def add_tag(self, tag: str):
        self.tags.append(tag)


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
        return self.roll() + self.to_hit + self.situational_bonus >= self.attack.target.ac


class HitArgs:
    def __init__(
        self,
        attack: AttackArgs,
        crit: bool = False,
        roll: int = 0,
    ):
        self._dmg = defaultdict(int)
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


class MissArgs:
    def __init__(self, attack: AttackArgs):
        self.attack = attack

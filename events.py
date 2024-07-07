import random
from target import Target
from weapons import Weapon
from collections import defaultdict


class AttackArgs:
    def __init__(
        self,
        character,
        target: Target,
        weapon: Weapon,
        main_action=False,
        light_attack: bool = False,
    ):
        self.character = character
        self.target = target
        self.weapon = weapon
        self.main_action = main_action
        self.light_attack = light_attack


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
            return self.roll1
        elif self.adv:
            return max(self.roll1, self.roll2)
        else:
            return min(self.roll1, self.roll2)

    def hits(self):
        return self.roll() + self.to_hit + self.situational_bonus >= self.target.ac


class HitArgs:
    def __init__(
        self,
        attack: AttackArgs,
        crit: bool = False,
    ):
        self._dmg = defaultdict(int)
        self.attack = attack
        self.crit = crit

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

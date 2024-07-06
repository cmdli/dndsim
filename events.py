import random
from target import Target
from weapons import Weapon


class AttackArgs:
    def __init__(self, target: Target, weapon: Weapon, main_action=False):
        self.target = target
        self.weapon = weapon
        self.main_action = main_action


class AttackRollArgs:
    def __init__(self, target):
        self.target = target
        self.adv = False
        self.disadv = False
        self.roll1 = random.randint(1, 20)
        self.roll2 = random.randint(1, 20)

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


class HitArgs:
    def __init__(
        self,
        target: Target,
        weapon: Weapon,
        crit: bool = False,
        main_action: bool = False,
    ):
        self.dmg = 0
        self.crit = crit
        self.target = target
        self.weapon = weapon
        self.main_action = main_action


class MissArgs:
    def __init__(self, target: Target, weapon: Weapon):
        self.target = target
        self.weapon = weapon

import random
from target import Target
from weapons import Weapon


class AttackRollArgs:
    def __init__(self, target=None):
        self.adv = False
        self.disadv = False
        self.target = target
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
        self, crit: bool = False, target: Target = None, weapon: Weapon = None
    ):
        self.dmg = 0
        self.crit = crit
        self.target = target
        self.weapon = weapon

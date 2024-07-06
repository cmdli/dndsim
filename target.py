import random
from util import prof_bonus

TARGET_AC = [
    13,  # 1
    13,  # 2
    13,  # 3
    14,  # 4
    15,  # 5
    15,  # 6
    15,  # 7
    16,  # 8
    16,  # 9
    17,  # 10
    17,  # 11
    17,  # 12
    18,  # 13
    18,  # 14
    18,  # 15
    18,  # 16
    19,  # 17
    19,  # 18
    19,  # 19
    19,  # 20
]


class Target:
    def __init__(self, level):
        self.ac = TARGET_AC[level - 1]
        self.prof = prof_bonus(level)
        if level >= 8:
            self.ability = 5
        elif level >= 4:
            self.ability = 4
        else:
            self.ability = 3
        self.save_bonus = self.prof + self.ability
        self.dmg = 0
        self.stunned = False
        self.stun_turns = 0
        self.grappled = False
        self.prone = False
        self.vexed = False

    def try_attack(self, to_hit):
        return random.randint(1, 20) + to_hit >= self.ac

    def damage(self, damage):
        self.dmg += damage

    def save(self, dc):
        return random.randint(1, 20) + self.save_bonus >= dc

    def stun(self):
        self.stun_turns = 1
        self.stunned = True

    def turn(self):
        if self.stunned:
            if self.stun_turns == 0:
                self.stunned = False
            else:
                self.stun_turns -= 1
        if self.prone:
            self.prone = False

    def grapple(self):
        self.grappled = True

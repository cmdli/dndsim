import random
from util import prof_bonus
from collections import defaultdict
from log import log

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
        self._dmg_log = defaultdict(int)
        self.stunned = False
        self.stun_turns = 0
        self.grappled = False
        self.prone = False

    def try_attack(self, to_hit):
        return random.randint(1, 20) + to_hit >= self.ac

    def damage(self, damage):
        self.dmg += damage

    def damage_source(self, source: str, damage: int):
        self.dmg += damage
        self._dmg_log[source] += damage

    def add_damage_sources(self, sources):
        for key in sources:
            self._dmg_log[key] += sources[key]
            self.dmg += sources[key]

    def print_damage_log(self):
        for key in self._dmg_log:
            print(f"Source: {key} - Damage: {self._dmg_log[key]}")

    def log_damage_sources(self):
        for key in self._dmg_log:
            log.record(f"Damage ({key})", self._dmg_log[key])

    def save(self, dc):
        roll = random.randint(1, 20)
        total = roll + self.save_bonus
        log.output(lambda : f"Save roll: {roll} total {total} vs {dc}")
        return total >= dc

    def turn(self):
        if self.prone:
            self.prone = False

    def grapple(self):
        self.grappled = True

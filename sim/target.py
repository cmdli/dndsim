import random
from util.util import prof_bonus
from collections import defaultdict
from util.log import log
from util.taggable import Taggable

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


class Target(Taggable):
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
        self.long_rest()

    def long_rest(self):
        self.dmg = 0
        self._dmg_log = defaultdict(int)
        self.short_rest()

    def short_rest(self):
        self.stunned = False
        self.stun_turns = 0
        self.grappled = False
        self.prone = False
        self.semistunned = False

    def damage_source(self, source: str, damage: int):
        self.dmg += damage
        self._dmg_log[source] += damage

    def log_damage_sources(self):
        for key in self._dmg_log:
            log.record(f"Damage ({key})", self._dmg_log[key])
        log.record(f"Damage (Total)", self.dmg)

    def save(self, dc):
        roll = random.randint(1, 20)
        total = roll + self.save_bonus
        log.output(lambda: f"Save roll: {roll} total {total} vs {dc}")
        return total >= dc

    def turn(self):
        if self.prone:
            self.prone = False

    def grapple(self):
        self.grappled = True

    def knock_prone(self):
        log.record("Knocked prone", 1)
        self.prone = True

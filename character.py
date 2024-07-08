from util import prof_bonus
from feats import Attack, Vex, Feat
from target import Target
from weapons import Weapon
from events import HitArgs, AttackRollArgs, AttackArgs, MissArgs
from log import log
from typing import List
from collections import defaultdict


class Character:
    def init(
        self,
        level=None,
        stats=None,
        feats=None,
        base_feats: List[Feat]=None,
        feat_schedule=[4, 8, 12, 16, 19],
        default_feats=None,
    ):
        if default_feats is None:
            default_feats = [Attack(), Vex()]
        self.level = level
        self.prof = prof_bonus(level)
        self.str = stats[0]
        self.dex = stats[1]
        self.con = stats[2]
        self.int = stats[3]
        self.wis = stats[4]
        self.cha = stats[5]
        self.minions = []
        self.feats = dict()
        self.feats_by_event = dict()
        for feat in default_feats:
            self.add_feat(feat)
        for feat in base_feats:
            self.add_feat(feat)
        for [target, feat] in zip(feat_schedule, feats):
            if level >= target:
                self.add_feat(feat)

    def add_feat(self, feat):
        feat.apply(self)
        self.feats[feat.name] = feat
        for event in feat.events():
            if event not in self.feats_by_event:
                self.feats_by_event[event] = []
            self.feats_by_event[event].append(feat)

    def has_feat(self, name: str):
        return name in self.feats

    def feat(self, name: str):
        return self.feats[name]

    def feats_for_event(self, event: str):
        if event not in self.feats_by_event:
            return []
        return self.feats_by_event[event]

    def has_feats_for_event(self, event: str):
        return event in self.feats_by_event

    def mod(self, stat: str):
        if stat == "none":
            return 0
        return (self.__getattribute__(stat) - 10) // 2

    def dc(self, stat: str):
        return self.mod(stat) + self.prof + 8

    def add_minion(self, minion):
        self.minions.append(minion)

    def remove_minion(self, minion):
        self.minions.remove(minion)

    def use_bonus(self, source: str):
        if not self.used_bonus:
            log.record(f"Bonus ({source})", 1)
            self.used_bonus = True
            return True
        return False

    def begin_turn(self, target: Target):
        log.record("Turn", 1)
        self.actions = 1
        self.used_bonus = False
        for feat in self.feats_for_event("begin_turn"):
            feat.begin_turn(target)

    def end_turn(self, target: Target):
        for feat in self.feats_for_event("end_turn"):
            feat.end_turn(target)
        if not self.used_bonus:
            log.record(f"Bonus (None)", 1)
        log.output(lambda: "")

    def turn(self, target: Target):
        self.begin_turn(target)
        self.before_action(target)
        while self.actions > 0:
            self.action(target)
            self.actions -= 1
        self.after_action(target)
        self.end_turn(target)
        for minion in self.minions:
            minion.turn(target)

    def before_action(self, target: Target):
        for feat in self.feats_for_event("before_action"):
            feat.before_action(target)

    def action(self, target: Target):
        for feat in self.feats_for_event("action"):
            feat.action(target)

    def after_action(self, target: Target):
        for feat in self.feats_for_event("after_action"):
            feat.after_action(target)

    def attack(
        self,
        target: Target,
        weapon: Weapon,
        tags: List[str] = [],
    ):
        args = AttackArgs(
            character=self,
            target=target,
            weapon=weapon,
            tags=tags,
        )
        for feat in self.feats_for_event("attack"):
            feat.attack(args)

    def before_attack(self):
        for feat in self.feats_for_event("before_attack"):
            feat.before_attack()

    def roll_attack(self, attack: AttackArgs, to_hit: int):
        args = AttackRollArgs(attack=attack, to_hit=to_hit)
        for feat in self.feats_for_event("roll_attack"):
            feat.roll_attack(args)
        return args

    def hit(
        self,
        attack: AttackArgs,
        crit: bool = False,
        roll: int = 0,
    ):
        args = HitArgs(attack=attack, crit=crit, roll=roll)
        for feat in self.feats_for_event("hit"):
            feat.hit(args)
        log.output(lambda: str(args._dmg))
        attack.target.add_damage_sources(args._dmg)

    def miss(self, attack: AttackArgs):
        args = MissArgs(attack)
        for feat in self.feats_for_event("miss"):
            feat.miss(args)

    def short_rest(self):
        for feat in self.feats_for_event("short_rest"):
            feat.short_rest()

    def long_rest(self):
        self.short_rest()
        for feat in self.feats_for_event("long_rest"):
            feat.long_rest()

    def enemy_turn(self, target: Target):
        for feat in self.feats_for_event("enemy_turn"):
            feat.enemy_turn(target)

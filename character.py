from util import prof_bonus
from feats import Attack
from target import Target
from weapons import Weapon
from events import HitArgs, AttackRollArgs, AttackArgs, MissArgs
from log import log


class Character:
    def init(
        self,
        level=None,
        stats=None,
        feats=None,
        base_feats=None,
        feat_schedule=[4, 8, 12, 16, 19],
    ):
        self.level = level
        self.prof = prof_bonus(level)
        self.str = stats[0]
        self.dex = stats[1]
        self.con = stats[2]
        self.int = stats[3]
        self.wis = stats[4]
        self.cha = stats[5]
        self.feats = []
        self.add_feat(Attack())
        for feat in base_feats:
            self.add_feat(feat)
        for [target, feat] in zip(feat_schedule, feats):
            if level >= target:
                self.add_feat(feat)

    def add_feat(self, feat):
        feat.apply(self)
        self.feats.append(feat)

    def has_feat(self, name: str):
        for feat in self.feats:
            if feat.name == name:
                return True
        return False

    def mod(self, stat: str):
        return (self.__getattribute__(stat) - 10) // 2

    def dc(self, stat: str):
        return self.mod(stat) + self.prof + 8

    def roll_attack(self, target: Target):
        args = AttackRollArgs(target=target)
        for feat in self.feats:
            feat.roll_attack(args)
        return args.roll()

    def hit(
        self,
        target: Target,
        weapon: Weapon,
        crit: bool = False,
        attack_args: AttackArgs = None,
    ):
        args = HitArgs(target, weapon, crit=crit, main_action=attack_args.main_action)
        for feat in self.feats:
            feat.hit(args)
        target.damage(args.dmg)

    def miss(self, target: Target, weapon: Weapon):
        args = MissArgs(target, weapon)
        for feat in self.feats:
            feat.miss(args)

    def enemy_turn(self, target: Target):
        for feat in self.feats:
            feat.enemy_turn(target)

    def begin_turn(self, target: Target):
        self.actions = 1
        self.used_bonus = False
        for feat in self.feats:
            feat.begin_turn(target)

    def turn(self, target: Target):
        self.begin_turn(target)
        while self.actions > 0:
            self.action(target)
            self.actions -= 1
        self.end_turn(target)

    def action(self, target: Target):
        for feat in self.feats:
            feat.action(target)

    def attack(self, target: Target, weapon: Weapon, main_action: bool = False):
        args = AttackArgs(target=target, weapon=weapon, main_action=main_action)
        for feat in self.feats:
            feat.attack(args)

    def end_turn(self, target: Target):
        for feat in self.feats:
            feat.end_turn(target)

    def short_rest(self):
        for feat in self.feats:
            feat.short_rest()

    def long_rest(self):
        self.short_rest()
        for feat in self.feats:
            feat.long_rest()

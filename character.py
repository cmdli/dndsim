from util import prof_bonus, do_roll
import random


class Feat:
    def apply(self, character):
        pass

    def begin_turn(self, target):
        pass

    def action(self, target, **kwargs):
        pass

    def attack(self, target, **kwargs):
        pass

    def roll_attack(self, args, **kwargs):
        pass

    def hit(self, target, **kwargs):
        pass

    def miss(self, target, **kwargs):
        pass

    def end_turn(self, target):
        pass

    def enemy_turn(self, target):
        pass

    def short_rest(self):
        pass

    def long_rest(self):
        pass


class AttackRollArgs:
    def __init__(self, adv=False, disadv=False, target=None):
        self.adv = adv
        self.disadv = disadv
        self.target = target


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
        self.feats = base_feats
        for feat in base_feats:
            feat.apply(self)
        for [target, feat] in zip(feat_schedule, feats):
            if level >= target:
                feat.apply(self)
                self.feats.append(feat)
        self.used_bonus = False

    def has_feat(self, name):
        for feat in self.feats:
            if feat.name == name:
                return True
        return False

    def mod(self, stat):
        return (self.__getattribute__(stat) - 10) // 2

    def dc(self, stat):
        return self.mod(stat) + self.prof + 8

    def roll_attack(self, target=None, adv=False, disadv=False):
        args = AttackRollArgs(adv=adv, disadv=disadv, target=target)
        args.roll1 = random.randint(1, 20)
        args.roll2 = random.randint(1, 20)
        for feat in self.feats:
            feat.roll_attack(args)
        if args.adv and args.disadv:
            return args.roll1
        elif args.adv:
            return max(args.roll1, args.roll2)
        elif args.disadv:
            return min(args.roll1, args.roll2)
        else:
            return args.roll1

    def hit(self, target, **kwargs):
        for feat in self.feats:
            feat.hit(target, **kwargs)

    def miss(self, target, **kwargs):
        for feat in self.feats:
            feat.miss(target, **kwargs)

    def enemy_turn(self, target):
        for feat in self.feats:
            feat.enemy_turn(target)

    def begin_turn(self, target):
        self.actions = 1
        self.used_bonus = False
        for feat in self.feats:
            feat.begin_turn(target)

    def turn(self, target, **kwargs):
        self.begin_turn(target)
        while self.actions > 0:
            self.action(target, **kwargs)
            self.actions -= 1
        self.end_turn(target)

    def action(self, target, **kwargs):
        for feat in self.feats:
            feat.action(target, **kwargs)

    def attack(self, target, **kwargs):
        for feat in self.feats:
            feat.attack(target, **kwargs)

    def end_turn(self, target):
        for feat in self.feats:
            feat.end_turn(target)

    def short_rest(self):
        for feat in self.feats:
            feat.short_rest()

    def long_rest(self):
        self.short_rest()
        for feat in self.feats:
            feat.long_rest()

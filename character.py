from util import prof_bonus
from feats import Attack, Vex
from target import Target
from weapons import Weapon
from events import HitArgs, AttackRollArgs, AttackArgs, MissArgs
from log import log
from typing import List


class Character:
    def init(
        self,
        level=None,
        stats=None,
        feats=None,
        base_feats=None,
        feat_schedule=[4, 8, 12, 16, 19],
        default_feats=[Attack(), Vex()],
    ):
        self.level = level
        self.prof = prof_bonus(level)
        self.str = stats[0]
        self.dex = stats[1]
        self.con = stats[2]
        self.int = stats[3]
        self.wis = stats[4]
        self.cha = stats[5]
        self.minions = []
        self.feats = []
        for feat in default_feats:
            self.add_feat(feat)
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

    def feat(self, name: str):
        for feat in self.feats:
            if feat.name == name:
                return feat
        return None

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

    def before_attack(self):
        for feat in self.feats:
            feat.before_attack()

    def roll_attack(self, target: Target, weapon: Weapon, to_hit: int):
        args = AttackRollArgs(target=target, weapon=weapon, to_hit=to_hit)
        for feat in self.feats:
            feat.roll_attack(args)
        return args

    def hit(
        self,
        target: Target,
        weapon: Weapon,
        crit: bool = False,
        attack_args: AttackArgs = None,
    ):
        log.output(lambda: "Hit with " + weapon.name + ", args " + str(attack_args))
        args = HitArgs(
            target,
            weapon,
            crit=crit,
            main_action=attack_args.main_action,
            light_attack=attack_args.light_attack,
        )
        for feat in self.feats:
            feat.hit(args)
        log.output(lambda: str(args._dmg))
        target.add_damage_sources(args._dmg)

    def miss(self, target: Target, weapon: Weapon):
        log.output(lambda: "Missed with " + weapon.name)
        args = MissArgs(target, weapon)
        for feat in self.feats:
            feat.miss(args)

    def enemy_turn(self, target: Target):
        for feat in self.feats:
            feat.enemy_turn(target)

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
        for feat in self.feats:
            feat.begin_turn(target)

    def end_turn(self, target: Target):
        for feat in self.feats:
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
        for feat in self.feats:
            feat.before_action(target)

    def action(self, target: Target):
        for feat in self.feats:
            feat.action(target)

    def after_action(self, target: Target):
        for feat in self.feats:
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
        for feat in self.feats:
            feat.attack(args)

    def before_attack(self):
        for feat in self.feats:
            feat.before_attack()

    def roll_attack(self, attack: AttackArgs, to_hit: int):
        args = AttackRollArgs(attack=attack, to_hit=to_hit)
        for feat in self.feats:
            feat.roll_attack(args)
        return args

    def hit(
        self,
        attack: AttackArgs,
        crit: bool = False,
        roll: int = 0,
    ):
        args = HitArgs(attack=attack, crit=crit, roll=roll)
        for feat in self.feats:
            feat.hit(args)
        attack.target.add_damage_sources(args._dmg)

    def miss(self, attack: AttackArgs):
        args = MissArgs(attack)
        for feat in self.feats:
            feat.miss(args)

    def short_rest(self):
        for feat in self.feats:
            feat.short_rest()

    def long_rest(self):
        self.short_rest()
        for feat in self.feats:
            feat.long_rest()

    def enemy_turn(self, target: Target):
        for feat in self.feats:
            feat.enemy_turn(target)

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
        attack_feat=Attack(),
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
        self.add_feat(attack_feat)
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
        args = HitArgs(
            target,
            weapon,
            crit=crit,
            main_action=attack_args.main_action,
            light_attack=attack_args.light_attack,
        )
        for feat in self.feats:
            feat.hit(args)
        target.add_damage_sources(args._dmg)

    def miss(self, target: Target, weapon: Weapon):
        args = MissArgs(target, weapon)
        for feat in self.feats:
            feat.miss(args)

    def enemy_turn(self, target: Target):
        for feat in self.feats:
            feat.enemy_turn(target)

    def begin_turn(self, target: Target):
        log.record("Turn", 1)
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
        for minion in self.minions:
            minion.turn(target)

    def action(self, target: Target):
        for feat in self.feats:
            feat.action(target)

    def attack(
        self,
        target: Target,
        weapon: Weapon,
        main_action: bool = False,
        light_attack: bool = False,
    ):
        args = AttackArgs(
            target=target,
            weapon=weapon,
            main_action=main_action,
            light_attack=light_attack,
        )
        for feat in self.feats:
            feat.attack(args)

    def end_turn(self, target: Target):
        for feat in self.feats:
            feat.end_turn(target)
        if not self.used_bonus:
            log.record(f"Bonus (None)", 1)

    def short_rest(self):
        for feat in self.feats:
            feat.short_rest()

    def long_rest(self):
        self.short_rest()
        for feat in self.feats:
            feat.long_rest()

    def use_bonus(self, source: str):
        if not self.used_bonus:
            log.record(f"Bonus ({source})", 1)
            self.used_bonus = True
            return True
        return False

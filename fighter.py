import random
from util import (
    prof_bonus,
    magic_weapon,
    do_roll,
    polearm_master,
    glaive,
    greatsword,
)
from feats import (
    GreatWeaponMaster,
    Greatsword,
    Glaive,
    Attack,
    AttackAction,
    ASI,
    PolearmMaster,
)
from character import Character, Feat


class StudiedAttacks(Feat):
    def __init__(self) -> None:
        self.name = "StudiedAttacks"
        self.enabled = False

    def roll_attack(self, args, **kwargs):
        args.adv = self.enabled

    def hit(self, target, **kwargs):
        self.enabled = False

    def miss(self, target, **kwargs):
        self.enabled = True


class HeroicAdvantage(Feat):
    def __init__(self):
        self.name = "HeroicAdvantage"

    def begin_turn(self, target):
        self.used = False

    def roll_attack(self, args, **kwargs):
        if self.used or args.adv:
            return
        if args.disadv:
            roll = min(args.roll1, args.roll2)
            if roll < 8:
                self.used = True
                self.adv = True
                args.roll1 = random.randint(1, 20)
        else:
            roll = args.roll1
            if roll < 8:
                self.used = True
                args.adv = True


class ActionSurge(Feat):
    def __init__(self, max_surges) -> None:
        self.name = "ActionSurge"
        self.max_surges = max_surges

    def apply(self, character):
        self.character = character

    def begin_turn(self, target):
        if self.surges > 0:
            self.character.actions += 1
            self.surges -= 1

    def short_rest(self):
        self.surges = self.max_surges


class Fighter(Character):
    def __init__(self, level, use_pam=False):
        base_feats = []
        self.use_pam = use_pam
        self.magic_weapon = magic_weapon(level)
        if level >= 20:
            base_feats.append(AttackAction(4))
        elif level >= 11:
            base_feats.append(AttackAction(3))
        elif level >= 5:
            base_feats.append(AttackAction(2))
        else:
            base_feats.append(AttackAction(1))
        if level >= 15:
            base_feats.append(Attack(mod="str", bonus=self.magic_weapon, min_crit=18))
        elif level >= 3:
            base_feats.append(Attack(mod="str", bonus=self.magic_weapon, min_crit=19))
        else:
            base_feats.append(Attack(mod="str", bonus=self.magic_weapon, min_crit=20))
        if level >= 13:
            base_feats.append(StudiedAttacks())
        if level >= 17:
            base_feats.append(ActionSurge(2))
        elif level >= 2:
            base_feats.append(ActionSurge(1))
        if use_pam:
            base_feats.append(
                Glaive(bonus=self.magic_weapon, savage_attacker=True, gwf=True)
            )
        else:
            base_feats.append(
                Greatsword(bonus=self.magic_weapon, savage_attacker=True, gwf=True)
            )
        if level >= 10:
            base_feats.append(HeroicAdvantage())
        feats = [
            GreatWeaponMaster(),
            ASI([["str", 2]]) if not use_pam else PolearmMaster(),
            ASI() if not use_pam else ASI([["str", 1]]),
            ASI(),
            ASI(),
            ASI(),
            ASI(),
        ]
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 10],
            feat_schedule=[4, 6, 8, 12, 14, 16, 19],
            feats=feats,
            base_feats=base_feats,
        )

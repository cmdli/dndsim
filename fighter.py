import random
from util import (
    magic_weapon,
)
from feats import (
    GreatWeaponMaster,
    AttackAction,
    ASI,
    PolearmMaster,
    Feat,
    EquipWeapon,
)
from character import Character
from weapons import Glaive, Greatsword, GlaiveButt


class StudiedAttacks(Feat):
    def __init__(self) -> None:
        self.name = "StudiedAttacks"
        self.enabled = False

    def roll_attack(self, args, **kwargs):
        args.adv = self.enabled

    def hit(self, args, **kwargs):
        self.enabled = False

    def miss(self, target, weapon, **kwargs):
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
        if level >= 15:
            min_crit = 18
        elif level >= 3:
            min_crit = 19
        else:
            min_crit = 20
        if use_pam:
            weapon = Glaive(bonus=self.magic_weapon, min_crit=min_crit)
        else:
            weapon = Greatsword(bonus=self.magic_weapon, min_crit=min_crit)
        base_feats.append(EquipWeapon(weapon, savage_attacker=True, max_reroll=2))
        if level >= 20:
            attacks = 4 * [weapon]
        elif level >= 11:
            attacks = 3 * [weapon]
        elif level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(AttackAction(attacks=attacks))
        if level >= 13:
            base_feats.append(StudiedAttacks())
        if level >= 17:
            base_feats.append(ActionSurge(2))
        elif level >= 2:
            base_feats.append(ActionSurge(1))
        if level >= 10:
            base_feats.append(HeroicAdvantage())
        if use_pam:
            feats = [
                GreatWeaponMaster(),
                PolearmMaster(GlaiveButt(bonus=self.magic_weapon)),
                ASI([["str", 1]]),
                ASI(),
                ASI(),
                ASI(),
                ASI(),
            ]
        else:
            feats = [
                GreatWeaponMaster(),
                ASI([["str", 2]]),
                ASI(),
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

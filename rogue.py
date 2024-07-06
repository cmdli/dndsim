import math
from util import (
    magic_weapon,
    roll_dice,
    do_roll,
)
from character import Character
from feats import ASI, AttackAction, Feat, EquipWeapon
from weapons import Shortsword, Scimitar
from log import log


class SneakAttack(Feat):
    def __init__(self, num):
        self.name = "SneakAttack"
        self.num = num

    def begin_turn(self, target):
        self.used = False

    def hit(self, args):
        if not self.used:
            self.used = True
            num = 2 * self.num if args.crit else self.num
            args.add_damage("SneakAttack", roll_dice(num, 6))


class SteadyAim(Feat):
    def __init__(self) -> None:
        self.name = "SteadyAim"

    def apply(self, character):
        self.character = character

    def begin_turn(self, target):
        if self.character.use_bonus("SteadyAim"):
            self.enabled = True

    def roll_attack(self, args):
        if self.enabled:
            args.adv = True

    def end_turn(self, target):
        self.enabled = False


class StrokeOfLuck(Feat):
    def __init__(self) -> None:
        self.name = "StrokeOfLuck"

    def begin_turn(self, target):
        self.used = False

    def roll_attack(self, args):
        if not self.used and args.roll() < 10:
            self.used = True
            args.roll1 = 20
            args.roll2 = 20


class Assassinate(Feat):
    def __init__(self, dmg):
        self.name = "Assassinate"
        self.dmg = dmg
        self.first_turn = False
        self.used_dmg = False
        self.adv = False

    def apply(self, character):
        self.character = character

    def short_rest(self):
        log.record("short_rest", 1)
        self.first_turn = True
        self.used_dmg = False

    def begin_turn(self, target):
        if self.first_turn:
            if do_roll(adv=True) + self.character.mod("dex") > do_roll():
                self.adv = True

    def roll_attack(self, args):
        if self.adv:
            args.adv = True

    def hit(self, args):
        if self.first_turn and not self.used_dmg:
            self.used_dmg = True
            args.add_damage("Assassinate", self.dmg)

    def end_turn(self, target):
        self.adv = False
        self.first_turn = False


class DeathStrike(Feat):
    def __init__(self) -> None:
        self.name = "DeathStrike"

    def apply(self, character):
        self.character = character

    def short_rest(self):
        self.enabled = True

    def hit(self, args):
        if self.enabled:
            self.enabled = False
            if not args.target.save(self.character.dc("dex")):
                args.add_damage("DeathStrike", args.total_damage())

    def end_turn(self, target):
        self.enabled = False


class Rogue(Character):
    def __init__(self, level):
        self.magic_weapon = magic_weapon(level)
        sneak_attack = math.ceil(level / 2)
        base_feats = []
        shortsword = Shortsword(bonus=self.magic_weapon)
        scimitar = Scimitar(bonus=self.magic_weapon)
        base_feats.append(EquipWeapon(shortsword))
        base_feats.append(EquipWeapon(scimitar))
        base_feats.append(AttackAction(attacks=[shortsword, scimitar]))
        base_feats.append(SneakAttack(sneak_attack))
        if level >= 3:
            base_feats.append(SteadyAim())
            base_feats.append(Assassinate(level))
        if level >= 17:
            base_feats.append(DeathStrike())
        if level >= 20:
            base_feats.append(StrokeOfLuck())
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 10, 10],
            feats=[ASI([["dex", 2]]), ASI([["dex", 1]])],
            base_feats=base_feats,
        )

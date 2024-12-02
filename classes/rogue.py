import math
from util.util import (
    get_magic_weapon,
    roll_dice,
    do_roll,
)
from sim.character import Character
from sim.feats import ASI, AttackAction, Feat, BoomingBlade, WeaponMasteries
from sim.weapons import Shortsword, Scimitar, Rapier
from util.log import log
from typing import List


class SneakAttack(Feat):
    def __init__(self, num):
        self.num = num

    def begin_turn(self, target):
        self.used = False

    def attack_result(self, args):
        if args.hits() and not self.used:
            self.used = True
            args.add_damage(source="SneakAttack", dice=self.num * [6])


class SteadyAim(Feat):
    def before_action(self, target):
        if self.character.use_bonus("SteadyAim"):
            self.enabled = True

    def attack_roll(self, args):
        if self.enabled:
            args.adv = True
            self.enabled = False

    def end_turn(self, target):
        self.enabled = False


class StrokeOfLuck(Feat):
    def begin_turn(self, target):
        self.used = False

    def attack_roll(self, args):
        if not self.used and args.roll() < 10:
            self.used = True
            args.roll1 = 20
            args.roll2 = 20


class Assassinate(Feat):
    def __init__(self, dmg):
        self.dmg = dmg
        self.first_turn = False
        self.used_dmg = False
        self.adv = False

    def short_rest(self):
        log.record("short_rest", 1)
        self.first_turn = True
        self.used_dmg = False

    def begin_turn(self, target):
        if self.first_turn:
            if do_roll(adv=True) + self.character.mod("dex") > do_roll():
                self.adv = True

    def attack_roll(self, args):
        if self.adv:
            args.adv = True

    def attack_result(self, args):
        if args.hits() and self.first_turn and not self.used_dmg:
            self.used_dmg = True
            args.add_damage(source="Assassinate", damage=self.dmg)

    def end_turn(self, target):
        self.adv = False
        self.first_turn = False


class DeathStrike(Feat):
    def short_rest(self):
        self.enabled = True

    def attack_result(self, args):
        if args.hits() and self.enabled:
            self.enabled = False
            if not args.attack.target.save(self.character.dc("dex")):
                args.dmg_multiplier *= 2

    def end_turn(self, target):
        self.enabled = False


class AssassinRogue(Character):
    def __init__(self, level: int, booming_blade: bool = False):
        magic_weapon = get_magic_weapon(level)
        sneak_attack = math.ceil(level / 2)
        base_feats: List[Feat] = []
        base_feats.append(WeaponMasteries(["vex", "nick"]))
        if level >= 5 and booming_blade:
            rapier = Rapier(magic_bonus=magic_weapon)
            base_feats.append(BoomingBlade(self, rapier))
        else:
            shortsword = Shortsword(magic_bonus=magic_weapon)
            scimitar = Scimitar(magic_bonus=magic_weapon)
            base_feats.append(
                AttackAction(attacks=[shortsword], nick_attacks=[scimitar])
            )
        base_feats.append(SneakAttack(sneak_attack))
        if level >= 3:
            base_feats.append(SteadyAim())
            base_feats.append(Assassinate(level))
        if level >= 4:
            base_feats.append(ASI(["dex"]))
        if level >= 8:
            base_feats.append(ASI(["dex", "wis"]))
        if level >= 17:
            base_feats.append(DeathStrike())
        if level >= 20:
            base_feats.append(StrokeOfLuck())
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 10, 10],
            base_feats=base_feats,
        )


class ArcaneTricksterRogue(Character):
    def __init__(self, level, **kwargs):
        magic_weapon = get_magic_weapon(level)
        sneak_attack = math.ceil(level / 2)
        base_feats = []
        base_feats.append(WeaponMasteries(["vex", "nick"]))
        base_feats.append(SneakAttack(sneak_attack))
        if level >= 3:
            base_feats.append(SteadyAim())
        if level >= 4:
            base_feats.append(ASI(["dex"]))
        if level >= 5:
            rapier = Rapier(magic_bonus=magic_weapon)
            base_feats.append(BoomingBlade(self, rapier))
        else:
            shortsword = Shortsword(magic_bonus=magic_weapon)
            scimitar = Scimitar(magic_bonus=magic_weapon)
            base_feats.append(
                AttackAction(attacks=[shortsword], nick_attacks=[scimitar])
            )
        if level >= 8:
            base_feats.append(ASI(["dex", "wis"]))
        if level >= 20:
            base_feats.append(StrokeOfLuck())
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 10, 10],
            base_feats=base_feats,
        )

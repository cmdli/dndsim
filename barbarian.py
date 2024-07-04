import random
from util import magic_weapon, do_roll, roll_dice
from character import (
    Character,
    Feat,
    AttackRollArgs,
)
from feats import (
    ASI,
    GreatWeaponMaster,
    Greatsword,
    Glaive,
    PolearmMaster,
)


class Beserker(Feat):
    def __init__(self, num_dice):
        self.name = "Berserker"
        self.used = False
        self.num_dice = num_dice

    def begin_turn(self, target):
        self.used = False

    def hit(self, target, crit=False, **kwargs):
        if not self.used:
            self.used = True
            target.damage(roll_dice(self.num_dice, 6))
            if crit:
                target.damage(roll_dice(self.num_dice, 6))


class BrutalStrike(Feat):
    def __init__(self, num_dice):
        self.name = "BrutalStrike"
        self.num_dice = num_dice

    def begin_turn(self, target):
        self.used = False

    def roll_attack(self, args: AttackRollArgs, **kwargs):
        if not self.used and args.adv:
            args.adv = False
            self.enabled = True
            self.used = True

    def hit(self, target, crit=False, **kwargs):
        if self.enabled:
            target.damage(roll_dice(self.num_dice, 10))
            if crit:
                target.damage(roll_dice(self.num_dice, 10))
        self.enabled = False

    def miss(self, target, **kwargs):
        self.enabled = False


class Retaliation(Feat):
    def __init__(self):
        self.name = "Retaliation"

    def apply(self, character):
        self.character = character

    def enemy_turn(self, target):
        self.character.attack(target)


class PrimalChampion(Feat):
    def __init__(self):
        self.name = "PrimalChampion"

    def apply(self, character):
        character.str += 4


class Rage(Feat):
    def __init__(self, dmg):
        self.name = "Rage"
        self.raging = False
        self.dmg = dmg

    def apply(self, character):
        self.character = character

    def short_rest(self):
        self.raging = False

    def begin_turn(self, target):
        if not self.raging and not self.character.used_bonus:
            self.character.used_bonus = True
            self.raging = True

    def hit(self, target, **kwargs):
        if self.raging:
            target.damage(self.dmg)


class RecklessAttack(Feat):
    def __init__(self):
        self.name = "RecklessAttack"

    def begin_turn(self, target):
        self.enabled = True

    def roll_attack(self, args: AttackRollArgs = None):
        args.adv = self.enabled

    def end_turn(self, target):
        self.enabled = False


class Barbarian(Character):
    def __init__(self, level, use_pam=False):
        if level >= 16:
            rage_dmg = 4
        elif level >= 9:
            rage_dmg = 3
        else:
            rage_dmg = 2
        self.magic_weapon = magic_weapon(level)
        base_feats = []
        base_feats.append(Rage(rage_dmg))
        base_feats.append(RecklessAttack())
        if level >= 3:
            base_feats.append(Beserker(rage_dmg))
        if level >= 17:
            base_feats.append(BrutalStrike(2))
        elif level >= 9:
            base_feats.append(BrutalStrike(1))
        if use_pam:
            base_feats.append(Glaive(self.magic_weapon))
        else:
            base_feats.append(Greatsword(self.magic_weapon))
        if level >= 10:
            base_feats.append(Retaliation())
        if level >= 20:
            base_feats.append(PrimalChampion())
        if use_pam:
            feats = [
                GreatWeaponMaster(),
                PolearmMaster(),
                ASI([["str", 1], ["con", 1]]),
                ASI(),
                ASI(),
            ]
        else:
            feats = [GreatWeaponMaster(), ASI([["str", 2]]), ASI(), ASI(), ASI()]
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 10],
            feats=feats,
            base_feats=base_feats,
        )
        if level >= 5:
            self.max_attacks = 2
        else:
            self.max_attacks = 1
        self.long_rest()

    def begin_turn(self, target):
        super().begin_turn(target)
        self.used_brutal_strike = False

    def turn(self, target):
        self.attacks = self.max_attacks
        while self.attacks > 0:
            self.attack(target)
            self.attacks -= 1

    def attack(self, target, pam=False):
        to_hit = self.prof + self.mod("str") + self.magic_weapon
        roll = self.roll_attack()
        if roll == 20:
            self.hit(target, crit=True, pam=pam)
        elif roll + to_hit >= target.ac:
            self.hit(target, pam=pam)
        else:
            self.miss(target)

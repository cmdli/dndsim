import random
from util import magic_weapon, do_roll, roll_dice
from character import Character
from feats import ASI, GreatWeaponMaster, PolearmMaster, AttackAction, Feat, EquipWeapon
from weapons import Glaive, Greatsword, GlaiveButt


class Beserker(Feat):
    def __init__(self, num_dice):
        self.name = "Berserker"
        self.used = False
        self.num_dice = num_dice

    def begin_turn(self, target):
        self.used = False

    def hit(self, args):
        if not self.used:
            self.used = True
            num = 2 * self.num_dice if args.crit else self.num_dice
            args.add_damage("Berserker", roll_dice(num, 6))


class BrutalStrike(Feat):
    def __init__(self, num_dice):
        self.name = "BrutalStrike"
        self.num_dice = num_dice

    def begin_turn(self, target):
        self.used = False

    def roll_attack(self, args):
        if not self.used and args.adv:
            args.adv = False
            self.enabled = True
            self.used = True

    def hit(self, args):
        if self.enabled:
            num = 2 * self.num_dice if args.crit else self.num_dice
            args.add_damage("BrutalStrike", roll_dice(num, 10))
        self.enabled = False

    def miss(self, args):
        self.enabled = False


class Retaliation(Feat):
    def __init__(self, weapon):
        self.name = "Retaliation"
        self.weapon = weapon

    def apply(self, character):
        self.character = character

    def enemy_turn(self, target):
        self.character.attack(target, weapon=self.weapon)


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
        if not self.raging and self.character.use_bonus("rage"):
            self.raging = True

    def hit(self, args):
        if self.raging:
            args.add_damage("Rage", self.dmg)


class RecklessAttack(Feat):
    def __init__(self):
        self.name = "RecklessAttack"

    def begin_turn(self, target):
        self.enabled = True

    def roll_attack(self, args):
        if self.enabled:
            args.adv = True

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
        if use_pam:
            weapon = Glaive(bonus=self.magic_weapon)
        else:
            weapon = Greatsword(bonus=self.magic_weapon)
        base_feats.append(EquipWeapon(weapon, savage_attacker=True))
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(AttackAction(attacks=attacks))
        if level >= 3:
            base_feats.append(Beserker(rage_dmg))
        if level >= 17:
            base_feats.append(BrutalStrike(2))
        elif level >= 9:
            base_feats.append(BrutalStrike(1))
        if level >= 10:
            base_feats.append(Retaliation(weapon))
        if level >= 20:
            base_feats.append(PrimalChampion())
        if use_pam:
            feats = [
                GreatWeaponMaster(),
                PolearmMaster(GlaiveButt(bonus=self.magic_weapon)),
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

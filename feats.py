from character import Feat
from util import roll_dice


class Weapon(Feat):
    def __init__(self, num_dice=0, size=6, mod="str", bonus=0, graze=False):
        self.name = "Weapon"
        self.num_dice = num_dice
        self.size = size
        self.mod = mod
        self.bonus = bonus
        self.graze = graze

    def apply(self, character):
        self.character = character

    def weapon(self, pam=False):
        if pam:
            return roll_dice(1, 4)
        return roll_dice(self.num_dice, self.size)

    def hit(self, target, crit=False, pam=False, **kwargs):
        target.damage(self.weapon(pam=pam) + self.character.mod(self.mod) + self.bonus)
        if crit:
            target.damage(self.weapon(pam=pam))

    def miss(self, target, **kwargs):
        if self.graze:
            target.damage(self.character.mod(self.mod))


class Glaive(Weapon):
    def __init__(self, bonus=0):
        super().__init__(num_dice=1, size=10, mod="str", bonus=bonus, graze=True)


class Greatsword(Weapon):
    def __init__(self, bonus=0):
        super().__init__(num_dice=2, size=6, mod="str", bonus=bonus, graze=True)


class PolearmMaster(Feat):
    def __init__(self):
        self.name = "PolearmMaster"

    def apply(self, character):
        self.character = character
        character.str += 1

    def begin_turn(self, target):
        self.used = False

    def end_turn(self, target):
        if not self.used and not self.character.used_bonus:
            self.used = True
            self.character.used_bonus = True
            self.character.attack(target, pam=True)


class GreatWeaponMaster(Feat):
    def __init__(self):
        self.name = "GreatWeaponMaster"

    def apply(self, character):
        character.str += 1
        self.character = character

    def begin_turn(self, target):
        self.used_dmg = False
        self.used_bonus_attack = False

    def hit(self, target, crit=False, **kwargs):
        if not self.used_dmg:
            self.used_dmg = True
            target.damage(self.character.prof)
        if crit and not self.used_bonus_attack and not self.character.used_bonus:
            self.character.attacks += 1
            self.character.used_bonus = True
            self.used_bonus_attack = True


class ASI(Feat):
    def __init__(self, stat_increases=[]):
        self.name = "ASI"
        self.stat_increases = stat_increases

    def apply(self, character):
        for [stat, increase] in self.stat_increases:
            character.__setattr__(stat, character.__getattribute__(stat) + increase)

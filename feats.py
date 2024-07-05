from character import Feat
from util import roll_dice


class Weapon(Feat):
    def __init__(
        self,
        num_dice=0,
        size=6,
        mod="str",
        bonus=0,
        graze=False,
        savage_attacker=False,
        max_reroll=0,
    ):
        self.name = "Weapon"
        self.num_dice = num_dice
        self.size = size
        self.mod = mod
        self.bonus = bonus
        self.graze = graze
        self.savage_attacker = savage_attacker
        self.max_reroll = max_reroll

    def apply(self, character):
        self.character = character

    def begin_turn(self, target):
        self.used_savage_attacker = False

    def weapon(self, pam=False):
        if pam:
            return roll_dice(1, 4, max_reroll=self.max_reroll)
        return roll_dice(self.num_dice, self.size, max_reroll=self.max_reroll)

    def damage(self, crit=False, pam=False):
        dmg = self.weapon(pam=pam)
        if crit:
            dmg += self.weapon(pam=pam)
        return dmg

    def hit(self, target, crit=False, pam=False, **kwargs):
        dmg = self.damage(crit=crit, pam=pam)
        if not self.used_savage_attacker and self.savage_attacker:
            self.used_savage_attacker = True
            dmg2 = self.damage(crit=crit, pam=pam)
            dmg = max(dmg, dmg2)
        target.damage(dmg + self.character.mod(self.mod) + self.bonus)

    def miss(self, target, **kwargs):
        if self.graze:
            target.damage(self.character.mod(self.mod))


class Glaive(Weapon):
    def __init__(self, **kwargs):
        super().__init__(num_dice=1, size=10, mod="str", graze=True, **kwargs)


class Greatsword(Weapon):
    def __init__(self, **kwargs):
        super().__init__(num_dice=2, size=6, mod="str", graze=True, **kwargs)


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


class AttackAction(Feat):
    def __init__(self, num_attacks):
        self.name = "AttackAction"
        self.num_attacks = num_attacks

    def apply(self, character):
        self.character = character

    def action(self, target):
        self.character.attacks = self.num_attacks
        while self.character.attacks > 0:
            self.character.attack(target, main_action=True)
            self.character.attacks -= 1


class Attack(Feat):
    def __init__(self, mod="str", bonus=0, min_crit=20):
        self.name = "Attack"
        self.mod = mod
        self.bonus = bonus
        self.min_crit = min_crit

    def apply(self, character):
        self.character = character

    def attack(self, target, **kwargs):
        roll = self.character.roll_attack(target=target)
        to_hit = self.character.prof + self.character.mod(self.mod) + self.bonus
        if roll >= self.min_crit:
            self.character.hit(target, crit=True, **kwargs)
        elif roll + to_hit >= target.ac:
            self.character.hit(target, **kwargs)
        else:
            self.character.miss(target)

import random
import math
from util import (
    prof_bonus,
    magic_weapon,
    cantrip_dice,
    highest_spell_slot,
    spell_slots,
    roll_dice,
    do_roll,
)


class Rogue:
    def __init__(self, level):
        self.level = level
        self.prof = prof_bonus(level)
        if level >= 8:
            self.dex = 5
        elif level >= 4:
            self.dex = 4
        else:
            self.dex = 3
        self.num_sneak_attack = math.ceil(level / 2)
        self.max_attacks = 2  # One plus dagger nick
        self.magic_weapon = magic_weapon(level)
        self.to_hit = self.prof + self.dex + self.magic_weapon
        self.dc = 8 + self.prof + self.dex
        self.long_rest()

    def weapon(self):
        return random.randint(1, 6)

    def begin_turn(self):
        self.used_bonus = False
        self.used_steady_aim = self.level < 3
        self.used_sneak_attack = False

    def turn(self, target):
        self.begin_turn()
        adv = self.assassinate_adv
        if not adv and not self.used_bonus and not self.used_steady_aim:
            adv = True
            self.used_bonus = True
            self.used_steady_aim = True
        self.attack(target, adv=adv, can_vex=True)
        self.attack(target, adv=adv)
        self.used_assassinate = True
        self.used_death_strike = True
        self.assassinate_adv = False

    def attack(self, target, adv=False, can_vex=False):
        if self.vex:
            adv = True
            self.vex = False
        roll = do_roll(adv=adv)
        if roll == 20:
            self.hit(target, crit=True, can_vex=can_vex)
        elif roll + self.to_hit >= target.ac:
            self.hit(target, can_vex=can_vex)
        else:
            if not self.used_stroke_of_luck:
                self.used_stroke_of_luck = True
                self.hit(target, crit=True, can_vex=can_vex)

    def hit(self, target, crit=False, can_vex=False):
        if can_vex:
            self.vex = True
        dmg = 0
        dmg += self.weapon() + self.dex + self.magic_weapon
        if crit:
            dmg += self.weapon()
        used_sneak_attack = False
        if not self.used_sneak_attack:
            used_sneak_attack = True
            self.used_sneak_attack = True
            dmg += roll_dice(self.num_sneak_attack, 6)
            if crit:
                dmg += roll_dice(self.num_sneak_attack, 6)
            if not self.used_assassinate:
                dmg += self.level
        if not self.used_death_strike and used_sneak_attack:
            self.used_death_strike = True
            if not target.save(self.dc):
                target.damage(dmg * 2)
            else:
                target.damage(dmg)
        else:
            target.damage(dmg)

    def short_rest(self):
        self.used_stroke_of_luck = self.level < 20
        self.used_assassinate = self.level < 3
        self.assassinate_adv = False
        if self.level >= 3 and do_roll(adv=True) + self.dex > do_roll():
            # We beat the target on initiative
            self.assassinate_adv = True
        self.used_death_strike = self.level < 17
        self.vex = False

    def long_rest(self):
        self.short_rest()

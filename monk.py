
import random
from util import prof_bonus, magic_weapon, cantrip_dice, highest_spell_slot, spell_slots, roll_dice, do_roll


class Monk:
    def __init__(self, level):
        self.level = level
        self.prof = prof_bonus(level)
        if level >= 20:
            self.dex = 7
        elif level >= 8:
            self.dex = 5
        elif level >= 4:
            self.dex = 4
        else:
            self.dex = 3
        if level >= 16:
            self.wis = 5
        elif level >= 12:
            self.wis = 4
        else:
            self.wis = 3
        self.magic_weapon = magic_weapon(level)
        self.to_hit = self.prof + self.dex + self.magic_weapon
        self.dc = self.prof + self.wis
        self.max_ki = 0
        if level >= 2:
            self.max_ki = level
        if level >= 17:
            self.weapon_die = 12
        elif level >= 11:
            self.weapon_die = 10
        elif level >= 5:
            self.weapon_die = 8
        else:
            self.weapon_die = 6
        self.action_attacks = 2 if level >= 5 else 1
        self.flurry_attacks = 3 if level >= 10 else 2
        self.short_rest()

    def weapon(self):
        r = random.randint(1, self.weapon_die)
        if r == 1:
            # Tavern brawler
            r = random.randint(1, self.weapon_die)
        return r
    
    def begin_turn(self):
        self.used_stun = self.level < 5
        self.used_grappler = self.level < 4

    def turn(self, target):
        self.begin_turn()
        for _ in range(self.action_attacks):
            self.attack(target, main_action=True)
        if self.ki > 0:
            self.ki -= 1
            for _ in range(self.flurry_attacks):
                self.attack(target)
        else:
            self.attack(target)

    def attack(self, target, main_action=False):
        roll = do_roll(target.stunned or target.grappled)
        if roll == 20:
            self.hit(target, crit=True, main_action=main_action)
        elif roll + self.to_hit >= target.ac:
            self.hit(target, main_action=main_action)

    def hit(self, target, crit=False, main_action=False):
        target.damage(self.weapon() + self.dex + self.magic_weapon)
        if crit:
            target.damage(self.weapon())
        if self.ki > 0 and not self.used_stun:
            # Stunning strike
            self.used_stun = True
            self.ki -= 1
            if target.save(self.dc):
                target.damage(self.weapon() + self.wis)
            else:
                target.stun()
        if main_action:
            target.grapple()

    def short_rest(self):
        self.ki = self.max_ki
    def long_rest(self):
        pass

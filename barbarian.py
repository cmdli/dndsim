
import random
from util import prof_bonus, magic_weapon, cantrip_dice, highest_spell_slot, spell_slots, roll_dice, do_roll

class Barbarian:
    def __init__(self, level, use_pam=False):
        self.level = level
        self.use_pam = use_pam
        self.prof = prof_bonus(level)
        if level >= 5:
            self.max_attacks = 2
        else:
            self.max_attacks = 1
        if level >= 20:
            self.str = 7
        elif level >= 12:
            self.str = 5
        elif level >= 8 and not use_pam:
            self.str = 5
        elif level >= 4:
            self.str = 4
        else:
            self.str = 3
        self.magic_weapon = magic_weapon(level)
        self.to_hit = self.prof + self.str + self.magic_weapon
        if level >= 16:
            self.rage_dmg = 4
        elif level >= 9:
            self.rage_dmg = 3
        else:
            self.rage_dmg = 2
        self.long_rest()

    def weapon(self, pam=False):
        if pam:
            return random.randint(1,4)
        elif self.use_pam:
            return random.randint(1,10)
        else:
            return random.randint(1,6) + random.randint(1,6)
    
    def brutal_strike_dmg(self):
        if self.level >= 17:
            return random.randint(1,10) + random.randint(1,10)
        return random.randint(1,10)

    def begin_turn(self):
        self.used_brutal_strike = self.level < 9
        self.used_gwm_dmg = self.level < 4
        self.used_gwm_bonus = self.level < 4
        self.used_bonus = False
        self.used_beserker = self.level < 3
        self.attacks = self.max_attacks

    def turn(self, target):
        self.begin_turn()
        if not self.raging and not self.used_bonus:
            self.raging = True
            self.used_bonus = True
        while self.attacks > 0:
            self.attack(target)
            self.attacks -= 1
        # Retaliation
        if self.level >= 10:
            self.attack(target, adv=False)
        if self.level >= 8 and self.use_pam and not self.used_bonus:
            self.attack(target, pam=True)

    def attack(self, target, adv=True, pam=False):
        brutal_strike = False
        if not self.used_brutal_strike:
            brutal_strike = True
            adv = False
            self.used_brutal_strike = True
        roll = do_roll(adv=adv)
        if roll == 20:
            self.hit(target, crit=True, brutal_strike=brutal_strike, pam=pam)
            if not self.used_bonus and not self.used_gwm_bonus:
                self.attacks += 1
                self.used_gwm_bonus = True
                self.used_bonus = True
        elif roll + self.to_hit >= target.ac:
            self.hit(target, brutal_strike=brutal_strike, pam=pam)
        else:
            target.damage(self.str)

    def hit(self, target, crit=False, brutal_strike=False, pam=False):
        target.damage(self.weapon(pam=pam) + self.str + self.magic_weapon)
        if self.raging:
            target.damage(self.rage_dmg)
        if crit:
            target.damage(self.weapon(pam=pam))
        if not self.used_gwm_dmg:
            target.damage(self.prof)
            self.used_gwm_dmg = True
        if not self.used_beserker:
            for _ in range(self.rage_dmg):
                target.damage(random.randint(1,6))
            if crit:
                for _ in range(self.rage_dmg):
                    target.damage(random.randint(1,6))
            self.used_beserker = True
        if brutal_strike:
            target.damage(self.brutal_strike_dmg())
            if crit:
                target.damage(self.brutal_strike_dmg())

    def short_rest(self):
        self.raging = False
    def long_rest(self):
        self.short_rest()

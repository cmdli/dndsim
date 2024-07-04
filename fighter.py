import random
from util import (
    prof_bonus,
    magic_weapon,
    do_roll,
    polearm_master,
    glaive,
    greatsword,
)


class Fighter:
    def __init__(self, level, use_pam=False):
        self.level = level
        self.use_pam = use_pam
        self.prof = prof_bonus(level)
        if level >= 6:
            self.str = 5
        elif level >= 4:
            self.str = 4
        else:
            self.str = 3
        self.magic_weapon = magic_weapon(self.level)
        self.to_hit = self.prof + self.str + self.magic_weapon
        self.gwm = self.prof
        if level >= 20:
            self.max_attacks = 4
        elif level >= 11:
            self.max_attacks = 3
        elif level >= 5:
            self.max_attacks = 2
        else:
            self.max_attacks = 1
        if level >= 15:
            self.min_crit = 18
        elif level >= 3:
            self.min_crit = 19
        else:
            self.min_crit = 20
        self.studied_attacks = False
        self.short_rest()

    def num_action_surge(self, level):
        if level >= 17:
            return 2
        elif level >= 2:
            return 1
        else:
            return 0

    def weapon(self, pam=False):
        if pam:
            # Polearm bonus attack
            return polearm_master(gwf=True)
        elif self.use_pam:
            return glaive(gwf=True)
        else:
            return greatsword(gwf=True)

    def begin_turn(self, target):
        self.actions = 1
        if self.action_surge >= 1:
            self.action_surge -= 1
            self.actions += 1
        self.used_savage_attacker = False
        self.used_bonus = False
        self.used_gwm_dmg = self.level < 4
        self.used_gwm_bonus = self.level < 4
        self.heroic_advantage = self.level >= 10

    def turn(self, target):
        for _ in range(self.actions):
            self.attacks = self.max_attacks
            while self.attacks > 0:
                self.attack(target)
                self.attacks -= 1
        global pam_used
        if self.level >= 8 and self.use_pam and not self.used_bonus:
            pam_used += 1
            self.attack(target, pam=True)

    def end_turn(self, target):
        pass

    def enemy_turn(self, target):
        pass

    def attack(self, target, pam=False):
        roll = do_roll(adv=self.studied_attacks)
        if self.studied_attacks:
            self.studied_attacks = False
        if self.heroic_advantage and roll + self.to_hit < target.ac:
            roll = random.randint(1, 20)
        if roll >= self.min_crit:
            if not self.used_gwm_bonus and not self.used_bonus:
                self.attacks += 1
                self.used_bonus = True
                self.used_gwm_bonus = True
            self.hit(target, crit=True, pam=pam)
        elif roll + self.to_hit >= target.ac:
            self.hit(target)
        else:
            target.damage(self.str)
            if self.level >= 13:
                self.studied_attacks = True

    def hit(self, target, crit=False, pam=False):
        weapon_roll = self.weapon(pam=pam)
        if not self.used_savage_attacker and weapon_roll <= 7:
            weapon_roll = self.weapon(pam=pam)
            self.used_savage_attacker = True
        target.damage(weapon_roll + self.str + self.magic_weapon)
        if crit:
            target.damage(self.weapon(pam=pam))
        if not self.used_gwm_dmg:
            target.damage(self.gwm)
            self.used_gwm_dmg = True

    def short_rest(self):
        self.action_surge = self.num_action_surge(self.level)

    def long_rest(self):
        pass

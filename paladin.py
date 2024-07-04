from util import (
    prof_bonus,
    magic_weapon,
    highest_spell_slot,
    spell_slots,
    do_roll,
    greatsword,
    gwf,
)


class Paladin:
    def __init__(self, level):
        self.level = level
        self.prof = prof_bonus(level)
        if level >= 5:
            self.max_attacks = 2
        else:
            self.max_attacks = 1
        if level >= 8:
            self.str = 5
        elif level >= 4:
            self.str = 4
        else:
            self.str = 3
        if level >= 16:
            self.cha = 5
        elif level >= 12:
            self.cha = 4
        else:
            self.cha = 3
        self.magic_weapon = magic_weapon(level)
        self.to_hit = self.prof + self.str + self.magic_weapon + self.cha
        self.long_rest()

    def weapon(self):
        return greatsword(gwf=self.level > 1)

    def begin_turn(self):
        self.used_bonus = False
        self.used_smite = self.level < 2
        self.attacks = self.max_attacks
        self.used_gwm_dmg = self.level < 4
        self.used_gwm_bonus = self.level < 4

    def turn(self, target):
        self.begin_turn()
        while self.attacks > 0:
            self.attack(target)
            self.attacks -= 1

    def attack(self, target):
        roll = do_roll()
        if roll == 20:
            self.hit(target, crit=True)
            if not self.used_gwm_bonus and not self.used_bonus:
                self.used_bonus = True
                self.used_gwm_bonus = True
                self.attacks += 1
        elif roll + self.to_hit >= target.ac:
            self.hit(target)
        else:
            # Graze
            target.damage(self.str)

    def hit(self, target, crit=False):
        target.damage(self.weapon() + self.str + self.magic_weapon)
        if crit:
            target.damage(self.weapon())
        if self.level >= 11:
            target.damage(gwf(1, 8))
            if crit:
                target.damage(gwf(1, 8))
        if not self.used_gwm_dmg:
            self.used_gwm_dmg = True
            target.damage(self.prof)
        slot = highest_spell_slot(self.slots)
        if not self.used_smite and not self.used_bonus and slot >= 1:
            self.used_bonus = True
            self.used_smite = True
            self.slots[slot] -= 1
            num_d8s = 1 + slot
            target.damage(gwf(num_d8s, 8))
            if crit:
                target.damage(gwf(num_d8s, 8))

    def long_rest(self):
        self.short_rest()
        self.slots = spell_slots(self.level, half=True)

    def short_rest(self):
        if self.level >= 11:
            self.channel_divinity = 3
        elif self.level >= 3:
            self.channel_divinity = 2

import random
from util import (
    prof_bonus,
    magic_weapon,
    highest_spell_slot,
    spell_slots,
    roll_dice,
    do_roll,
)


class Ranger:
    def __init__(self, level):
        self.level = level
        self.prof = prof_bonus(level)
        if level >= 8:
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
        self.to_hit = self.prof + self.dex + self.magic_weapon + 2
        self.spell_hit = self.prof + self.wis + self.magic_weapon
        if level >= 5:
            self.max_attacks = 2
        else:
            self.max_attacks = 1

    def weapon(self):
        return random.randint(1, 6)

    def hunters_mark(self):
        if self.level >= 20:
            return random.randint(1, 10)
        return random.randint(1, 6)

    def begin_turn(self):
        self.used_bonus = False
        self.attacks = self.max_attacks
        self.used_natures_veil = False

    def turn(self, target):
        self.begin_turn()
        slot = highest_spell_slot(self.slots)
        if slot >= 4 and not self.concentration:
            self.fey_summon = slot
            self.concentration = True
            self.slots[slot] -= 1
        else:
            if (
                not self.used_bonus
                and not self.used_hunters_mark
                and not self.concentration
            ):
                self.used_bonus = True
                self.used_hunters_mark = True
                self.concentration = True
            # Nature's Veil is DPR loss
            # if self.level >= 14 and self.level < 17 and not self.used_bonus and not self.used_natures_veil:
            #     self.used_bonus = True
            #     self.used_natures_veil = True
            while self.attacks > 0:
                self.attack(target)
                self.attacks -= 1
            if self.level >= 3 and not self.used_gloom_attack:
                self.used_gloom_attack = True
                self.attack(target, gloom=True)
            if not self.used_bonus and self.level >= 4:
                self.used_bonus = True
                self.attack(target, bonus=True)
        if self.fey_summon > 0:
            self.summon_fey(target)

    def attack(self, target, bonus=False, gloom=False):
        adv = False
        if self.level >= 17 and self.used_hunters_mark:
            adv = True
        if self.used_natures_veil:
            adv = True
        if self.vex:
            adv = True
            self.vex = False
        roll = do_roll(adv=adv)
        if roll == 20:
            self.hit(target, crit=True, bonus=bonus, gloom=gloom)
        elif roll + self.to_hit >= target.ac:
            self.hit(target, bonus=bonus, gloom=gloom)

    def hit(self, target, crit=False, bonus=False, gloom=False):
        self.vex = True
        target.damage(self.weapon() + self.magic_weapon)
        if not bonus or self.level >= 4:
            target.damage(self.dex)
        if crit:
            target.damage(self.weapon())
        if gloom:
            target.damage(random.randint(1, 8))
            if crit:
                target.damage(random.randint(1, 8))
        if self.used_hunters_mark:
            target.damage(self.hunters_mark())
            if crit:
                target.damage(self.hunters_mark())

    def summon_fey(self, target):
        adv = True  # Advantage on first attack
        num_attacks = self.fey_summon // 2
        for _ in range(num_attacks):
            roll = do_roll(adv=adv)
            adv = False
            if roll == 20:
                target.damage(roll_dice(4, 6) + 3 + self.fey_summon)
            elif roll + self.to_hit >= target.ac:
                target.damage(roll_dice(2, 6) + 3 + self.fey_summon)

    def long_rest(self):
        self.short_rest()
        # level = self.level
        # if level == 20: # Ranger multiclass at 20
        #     level += 2
        self.slots = spell_slots(self.level, half=True)

    def short_rest(self):
        self.vex = False
        self.used_gloom_attack = False
        self.used_hunters_mark = False
        self.concentration = False
        self.fey_summon = 0

import random
from util import prof_bonus, magic_weapon, cantrip_dice, highest_spell_slot, spell_slots, roll_dice, do_roll

class Cleric:
    def __init__(self, level):
        self.level = level
        self.prof = prof_bonus(level)
        if level >= 8:
            self.wis = 5
        elif level >= 4:
            self.wis = 4
        else:
            self.wis = 3
        if level >= 19:
            self.str = 5
        elif level >= 16:
            self.str = 4
        else:
            self.str = 3
        self.magic_weapon = magic_weapon(level)
        self.spell_hit = self.prof + self.wis
        self.to_hit = self.prof + self.str + self.magic_weapon
        self.dc = 8 + self.prof + self.wis
        self.cantrip_dice = cantrip_dice(level)
        if level >= 18:
            self.max_channel_divinity = 4
        elif level >= 6:
            self.max_channel_divinity = 3
        else:
            self.max_channel_divinity = 2
        self.long_rest()

    def long_rest(self):
        self.slots = spell_slots(self.level)
        self.channel_divinity = self.max_channel_divinity
        self.short_rest()
    
    def short_rest(self):
        self.concentration = False
        self.spirit_weap = 0
        self.guardians = 0
        self.celestial_summon = 0
        if self.channel_divinity < self.max_channel_divinity:
            self.channel_divinity += 1
        self.war_priest = self.wis

    def begin_turn(self):
        self.used_bonus = False
        self.used_reaction = False
        self.used_gwm_dmg = self.level < 12

    def turn(self, target):
        self.begin_turn()
        slot = highest_spell_slot(self.slots)
        if not self.concentration and slot >= 3:
            if slot >= 5 and self.celestial_summon == 0:
                self.celestial_summon = slot
                self.concentration = True
            elif slot >= 3 and self.guardians == 0:
                self.guardians = slot
                self.concentration = True
            self.slots[slot] -= 1
        # elif self.spirit_weap == 0 and self.level >= 3:
        #     slot = highest_spell_slot(self.slots, max=4)
        #     if self.spirit_weap == 0:
        #         self.spirit_weap = slot
        #         self.slots[slot] -= 1
        #         self.toll_the_dead(target)
        #     if slot > 0:
        #         self.slots[slot] -= 1
        else:
            slot = highest_spell_slot(self.slots, max=5)
            if slot >= 6:
                self.harm(target, slot)
            elif slot >= 1:
                self.inflict_wounds(target, slot)
            else:
                self.toll_the_dead(target)
            if slot > 0:
                self.slots[slot] -= 1
        if self.guardians > 0:
            self.spirit_guardians(target, self.guardians)
        if self.celestial_summon > 0:
            self.summon_celestial(target, self.celestial_summon)
        if self.spirit_weap > 0:
            self.spiritual_weapon(target, self.spirit_weap)
            self.used_bonus = True
        if not self.used_bonus and self.war_priest > 0:
            self.used_bonus = True
            self.war_priest -= 1
            self.attack(target)

    def harm(self, target, slot):
        dmg = roll_dice(14,6)
        if target.save(self.dc):
            target.damage(dmg//2)
        else:
            target.damage(dmg)

    def inflict_wounds(self, target, slot):
        num_dice = 2 + slot
        roll = do_roll()
        if roll == 20:
            num_dice *= 2
        if roll + self.spell_hit >= target.ac:
            target.damage(roll_dice(num_dice,10)+roll_dice(1,8))
        elif self.level >= 3 and not self.used_reaction and self.channel_divinity > 0:
            self.channel_divinity -= 1
            self.used_reaction = True
            if roll + self.spell_hit + 10 >= target.ac:
                target.damage(roll_dice(num_dice,10)+roll_dice(1,8))

    def spiritual_weapon(self, target, slot):
        num_dice = slot // 2
        roll = do_roll()
        if roll == 20:
            num_dice *= 2
        if roll + self.spell_hit >= target.ac:
            target.damage(roll_dice(num_dice,8)+self.wis)
    
    def spirit_guardians(self, target, slot):
        dmg = roll_dice(2+slot,8)
        if target.save(self.dc):
            target.damage(dmg//2)
        else:
            target.damage(dmg)

    def summon_celestial(self, target, slot):
        for _ in range(slot//2):
            roll = do_roll()
            if roll == 20:
                target.damage(roll_dice(4,6)+2+slot)
            elif roll + self.spell_hit >= target.ac:
                target.damage(roll_dice(2,6)+2+slot)
    
    def toll_the_dead(self, target):
        if not target.save(self.dc):
            target.damage(roll_dice(self.cantrip_dice, 12)+roll_dice(1,8))
    
    def attack(self, target):
        roll = do_roll()
        if roll == 20:
            target.damage(random.randint(4,6)+self.str+self.magic_weapon)
            if not self.used_gwm_dmg:
                target.damage(self.prof)
                self.used_gwm_dmg = True
        elif roll + self.to_hit >= target.ac:
            target.damage(random.randint(2,6)+self.str+self.magic_weapon)
            if not self.used_gwm_dmg:
                target.damage(self.prof)
                self.used_gwm_dmg = True
        else:
            target.damage(self.str)


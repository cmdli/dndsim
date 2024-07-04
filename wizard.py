import random
from util import prof_bonus, magic_weapon, cantrip_dice, highest_spell_slot, spell_slots, roll_dice, do_roll

class Wizard:
    def __init__(self, level):
        self.level = level
        self.prof = prof_bonus(level)
        if level >= 8:
            self.int = 5
        elif level >= 4:
            self.int = 4
        else:
            self.int = 3
        self.dc = 8 + self.prof + self.int
        self.magic_weapon = magic_weapon(level)
        self.to_hit = self.prof + self.int + self.magic_weapon
        self.cantrip_dice = cantrip_dice(level)
        self.long_rest()

    def long_rest(self):
        self.short_rest()
        self.slots = spell_slots(self.level)
        self.used_arcane_recovery = False
        self.used_overchannel = self.level < 14

    def short_rest(self):
        # TODO: use arcane recovery
        self.concentration = False
        self.fey_summon = 0

    def turn(self, target):
        slot = highest_spell_slot(self.slots)
        if slot >= 3 and not self.concentration:
            self.fey_summon = slot
            self.concentration = True
        else:
            if slot >= 9:
                self.meteor_swarm(target)
            elif slot >= 7:
                self.finger_of_death(target)
            elif slot >= 6:
                self.chain_lightning(target)
            elif slot >= 5 and not self.used_overchannel:
                self.blight(target, slot, overchannel=True)
                self.used_overchannel = True
            elif slot >= 4:
                self.blight(target, slot)
            elif slot >= 3:
                self.fireball(target, slot)
            elif slot >= 2 and self.level < 11:
                self.scorching_ray(target, slot)
            elif slot >= 1 and self.level < 5:
                self.magic_missile(target, slot)
            else:
                self.firebolt(target)
        if slot >= 1:
            self.slots[slot] -= 1
        if self.fey_summon > 0:
            self.summon_fey(target)

    def meteor_swarm(self, target):
        dmg = roll_dice(40,6)+self.int
        if target.save(self.dc):
            target.damage(dmg // 2)
        else:
            target.damage(dmg)

    def finger_of_death(self, target):
        dmg = roll_dice(7,8)+30
        if target.save(self.dc):
            target.damage(dmg // 2)
        else:
            target.damage(dmg)

    def chain_lightning(self, target):
        dmg = roll_dice(10,8)+self.int
        if target.save(self.dc):
            target.damage(dmg//2)
        else:
            target.damage(dmg)

    def disintegrate(self, target, slot):
        if not target.save(self.dc):
            target.damage(40+roll_dice(10 + (slot-6),6))

    def steel_wind_strike(self, target):
        roll = do_roll()
        if roll == 20:
            target.damage(roll_dice(12,10))
        elif roll + self.to_hit >= target.ac:
            target.damage(roll_dice(6,10))

    def blight(self, target, slot, overchannel=False):
        num_dice = 8 + (slot - 4)
        if overchannel:
            dmg = num_dice * 8
        else:
            dmg = roll_dice(num_dice,8)
        if target.save(self.dc):
            target.damage(dmg//2)
        else:
            target.damage(dmg)

    def scorching_ray(self, target, slot):
        for _ in range(3+(slot - 2)):
            roll = do_roll()
            if roll == 20:
                target.damage(roll_dice(4,6))
            elif roll + self.to_hit >= target.ac:
                target.damage(roll_dice(2,6))
        target.damage(self.int)

    def fireball(self, target, slot):
        dmg = roll_dice(8 + (slot - 3),6)+self.int
        if not target.save(self.dc):
            target.damage(dmg)
        else:
            target.damage(dmg // 2)
    
    def erupting_earth(self, target, slot):
        dmg = roll_dice(3 + (slot - 3),12)
        if target.save(self.dc):
            target.damage(dmg)
        else:
            target.damage(dmg//2)

    def magic_missile(self, target, slot):
        target.damage(roll_dice(3+(slot-1),4)+self.int)

    def firebolt(self, target, adv=False):
        roll = do_roll(adv=adv)
        num_dice = self.cantrip_dice
        if roll == 20:
            num_dice *= 2
        dmg = roll_dice(num_dice,10)+self.int
        if roll + self.to_hit >= target.ac:
            target.damage(dmg)
        elif self.level >= 2:
            target.damage(dmg//2)

    def summon_fey(self, target):
        adv = True # Advantage on first attack
        num_attacks = self.fey_summon//2
        for _ in range(num_attacks):
            roll = do_roll(adv=adv)
            adv = False
            if roll == 20:
                target.damage(roll_dice(4,6)+3+self.fey_summon)
            elif roll + self.to_hit >= target.ac:
                target.damage(roll_dice(2,6)+3+self.fey_summon)

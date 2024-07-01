
import random
import math

NUM_FIGHTS = 3
NUM_TURNS = 5
NUM_SIMS = 100

SPELL_SLOTS_ARR = [
    [0,0,0,0,0,0,0,0,0,0], # 0
    [0,2,0,0,0,0,0,0,0,0], # 1
    [0,3,0,0,0,0,0,0,0,0], # 2
    [0,4,2,0,0,0,0,0,0,0], # 3
    [0,4,3,0,0,0,0,0,0,0], # 4
    [0,4,3,2,0,0,0,0,0,0], # 5
    [0,4,3,3,0,0,0,0,0,0], # 6
    [0,4,3,3,1,0,0,0,0,0], # 7
    [0,4,3,3,2,0,0,0,0,0], # 8
    [0,4,3,3,3,1,0,0,0,0], # 9
    [0,4,3,3,3,2,0,0,0,0], # 10
    [0,4,3,3,3,2,1,0,0,0], # 11
    [0,4,3,3,3,2,1,0,0,0], # 12
    [0,4,3,3,3,2,1,1,0,0], # 13
    [0,4,3,3,3,2,1,1,0,0], # 14
    [0,4,3,3,3,2,1,1,1,0], # 15
    [0,4,3,3,3,2,1,1,1,0], # 16
    [0,4,3,3,3,2,1,1,1,1], # 17
    [0,4,3,3,3,3,1,1,1,1], # 18
    [0,4,3,3,3,3,2,1,1,1], # 19
    [0,4,3,3,3,3,2,2,1,1], # 20
]
def spell_slots(level, half=False):
    if half:
        level = math.ceil(level / 2)
    return SPELL_SLOTS_ARR[level].copy()

def prof_bonus(level):
    return ((level-1) // 4) + 2

def magic_weapon(level):
    if level >= 15:
        return 3
    elif level >= 10:
        return 2
    elif level >= 5:
        return 1
    return 0

def do_roll(adv=False, disadv=False):
    if adv and disadv:
        return random.randint(1,20)
    elif adv:
        return max(random.randint(1,20), random.randint(1,20))
    elif disadv:
        return min(random.randint(1,20), random.randint(1,20))
    return random.randint(1,20)

def roll_dice(num, size):
    total = 0
    for _ in range(num):
        total += random.randint(1,size)
    return total

def highest_spell_slot(slots):
    # Finds the highest level spell slot available
    slot = len(slots) - 1
    while slot > 0:
        if slots[slot] > 0:
            return slot
        slot -= 1
    return -1

def cantrip_dice(level):
    if level >= 17:
        return 4
    elif level >= 11:
        return 3
    elif level >= 5:
        return 2
    return 1

def polearm_master(gwf=False):
    r = random.randint(1,4)
    if gwf and (r == 1 or r == 2):
        r = random.randint(1,4)
    return r

def glaive(gwf=False):
    r = random.randint(1,10)
    if gwf and (r == 1 or r == 2):
        r = random.randint(1,10)
    return r

def greatsword(gwf=False):
    r1 = random.randint(1,6)
    if gwf and (r1 == 1 or r1 == 2):
        r1 = random.randint(1,6)
    r2 = random.randint(1,6)
    if gwf and (r2 == 1 or r2 == 2):
        r2 = random.randint(1,6)
    return r1 + r2

def gwf(count, size):
    total = 0
    for _ in range(count):
        r = random.randint(1,size)
        if r == 1 or r == 2:
            r = random.randint(1,size)
        total += r
    return total


class Target:
    def __init__(self, level):
        self.ac = 13 + (level // 2)
        self.prof = prof_bonus(level)
        if level >= 8:
            self.ability = 5
        elif level >= 4:
            self.ability = 4
        else:
            self.ability = 3
        self.save_bonus = self.prof + self.ability
        self.dmg = 0
        self.stunned = False
        self.stun_turns = 0
        self.grappled = False
        self.prone = False

    def try_attack(self, to_hit):
        return random.randint(1,20)+to_hit >= self.ac

    def damage(self, damage):
        self.dmg += damage

    def save(self, dc):
        return random.randint(1,20) + self.save_bonus >= dc
    
    def stun(self):
        self.stun_turns = 1
        self.stunned = True

    def turn(self):
        if self.stunned:
            if self.stun_turns == 0:
                self.stunned = False
            else:
                self.stun_turns -= 1
        if self.prone:
            self.prone = False
    
    def grapple(self):
        self.grappled = True

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
    
    def begin_turn(self):
        self.actions = 1
        if self.action_surge >= 1:
            self.action_surge -= 1
            self.actions += 1
        self.used_savage_attacker = False
        self.used_bonus = False
        self.used_gwm_dmg = self.level < 4
        self.used_gwm_bonus = self.level < 4
        self.heroic_advantage = self.level >= 10

    def turn(self, target: Target):
        self.begin_turn()
        for _ in range(self.actions):
            self.attacks = self.max_attacks
            while self.attacks > 0:
                self.attack(target)
                self.attacks -= 1
        global pam_used
        if self.level >= 8 and self.use_pam and not self.used_bonus:
            pam_used += 1
            self.attack(target, pam=True)

    def attack(self, target, pam=False):
        roll = do_roll(adv=self.studied_attacks)
        if self.studied_attacks:
            self.studied_attacks = False
        if self.heroic_advantage and roll + self.to_hit < target.ac:
            roll = random.randint(1,20)
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
        target.damage(self.weapon(pam=pam) + self.str + self.rage_dmg + self.magic_weapon)
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
        pass
    def long_rest(self):
        pass

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
                target.damage(gwf(1,8))
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
        self.slots = spell_slots(level, half=True)

    def short_rest(self):
        if self.level >= 11:
            self.channel_divinity = 3
        elif self.level >= 3:
            self.channel_divinity = 2

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
        self.magic_weapon = magic_weapon(level)
        self.to_hit = self.prof + self.dex + self.magic_weapon + 2
        if level >= 5:
            self.max_attacks = 2
        else:
            self.max_attacks = 1

    def weapon(self):
        return random.randint(1,6)
    
    def hunters_mark(self):
        if self.level >= 20:
            return random.randint(1,10)
        return random.randint(1,6)

    def begin_turn(self):
        self.used_bonus = False
        self.attacks = self.max_attacks
        self.used_natures_veil = False

    def turn(self, target):
        self.begin_turn()
        if not self.used_bonus and not self.used_hunters_mark:
            self.used_bonus = True
            self.used_hunters_mark = True
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
            target.damage(random.randint(1,8))
            if crit:
                target.damage(random.randint(1,8))
        if self.used_hunters_mark:
            target.damage(self.hunters_mark())
            if crit:
                target.damage(self.hunters_mark())

    def long_rest(self):
        self.used_hunters_mark = False
        self.short_rest()
        self.slots = spell_slots(level, half=True)

    def short_rest(self):
        self.vex = False
        self.used_gloom_attack = False

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
        self.max_attacks = 2 # One plus dagger nick
        self.magic_weapon = magic_weapon(level)
        self.to_hit = self.prof + self.dex + self.magic_weapon
        self.dc = 8 + self.prof + self.dex
        self.long_rest()

    def weapon(self):
        return random.randint(1,6)

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
                target.damage(dmg*2)
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
        self.slots = spell_slots(level)
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


def simulate(character, level, fights, turns):
    dmg = 0
    character.long_rest()
    for _ in range(fights):
        target = Target(level)
        for _ in range(turns):
            character.turn(target)
            target.turn()
        character.short_rest()
        dmg += target.dmg
    return dmg

def test_dpr(character):
    damage = 0
    for _ in range(NUM_SIMS):
        damage += simulate(character, level, NUM_FIGHTS, NUM_TURNS)
    return damage/(NUM_SIMS*NUM_FIGHTS*NUM_TURNS)


if __name__ == "__main__":
    for level in range(1,21):
        fighter_damage = test_dpr(Fighter(level))
        barbarian_damage = test_dpr(Barbarian(level))
        monk_damage = test_dpr(Monk(level))
        paladin_damage = test_dpr(Paladin(level))
        ranger_dmage = test_dpr(Ranger(level))
        rogue_damage = test_dpr(Rogue(level))
        wizard_damage = test_dpr(Wizard(level))
        print(f"Level {level} -- Fighter: {fighter_damage:0.2f} DPR - Monk: {monk_damage:0.2f} DPR - Barbarian: {barbarian_damage:0.2f} DPR - Paladin: {paladin_damage:0.2f} DPR - Ranger: {ranger_dmage:0.2f} DPR - Rogue: {rogue_damage:0.2f} DPR - Wizard: {wizard_damage:0.2f} DPR")


        # fighter_damage = test_dpr(Fighter(level))
        # fighter_pam_damage = test_dpr(Fighter(level, True))
        # print(f"Fighter (greatsword) {level}: {fighter_damage:0.2f} DPR - Fighter (glaive) {level}: {fighter_pam_damage:0.2f} DPR")

        # barbarian_damage = test_dpr(Barbarian(level))
        # barbarian_pam_damage = test_dpr(Barbarian(level, True))
        # print(f"Barbarian (greatsword) {level}: {barbarian_damage:0.2f} DPR - Barbarian (glaive) {level}: {barbarian_pam_damage:0.2f} DPR")

        # wizard_damage = test_dpr(Wizard(level))
        # print(f"Level {level} -- Wizard: {wizard_damage:0.2f} DPR")
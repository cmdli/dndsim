
import random
import math

NUM_FIGHTS = 3
NUM_TURNS = 5
NUM_SIMS = 200

weapon_hits = 0

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
        return random.randint(1,self.weapon_die)
    
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

class Fighter:
    def __init__(self, level):
        self.level = level
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

    def weapon(self):
        return random.randint(1,6) + random.randint(1,6)
    
    def begin_turn(self):
        self.actions = 1
        if self.action_surge >= 1:
            self.action_surge -= 1
            self.actions += 1
        self.used_savage_attacker = False
        self.used_gwm = self.level < 4
        self.used_bonus = self.level < 4
        self.heroic_advantage = self.level >= 10

    def turn(self, target: Target):
        self.begin_turn()
        for _ in range(self.actions):
            self.attacks = self.max_attacks
            while self.attacks > 0:
                self.attack(target)
                self.attacks -= 1

    def attack(self, target):
        roll = do_roll(adv=self.studied_attacks)
        if self.studied_attacks:
            self.studied_attacks = False
        if self.heroic_advantage and roll + self.to_hit < target.ac:
            roll = random.randint(1,20)
        if roll >= self.min_crit:
            if not self.used_bonus:
                self.attacks += 1
                self.used_bonus = True
            self.hit(target, True)
        elif roll + self.to_hit >= target.ac:
            self.hit(target)
        else:
            target.damage(self.str)
            if self.level >= 13:
                self.studied_attacks = True


    def hit(self, target, crit=False):
        weapon_roll = self.weapon()
        if not self.used_savage_attacker and weapon_roll <= 7:
            weapon_roll = self.weapon()
            self.used_savage_attacker = True
        target.damage(self.weapon() + self.str + self.magic_weapon)
        if crit:
            target.damage(self.weapon())
        if not self.used_gwm:
            target.damage(self.gwm)
            self.used_gwm = True

    def short_rest(self):
        self.action_surge = self.num_action_surge(self.level)

class Barbarian:
    def __init__(self, level):
        self.level = level
        self.prof = prof_bonus(level)
        if level >= 5:
            self.max_attacks = 2
        else:
            self.max_attacks = 1
        if level >= 20:
            self.str = 7
        elif level >= 8:
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

    def weapon(self):
        return random.randint(1,6) + random.randint(1,6)
    
    def brutal_strike_dmg(self):
        if self.level >= 17:
            return random.randint(1,10) + random.randint(1,10)
        return random.randint(1,10)

    def begin_turn(self):
        self.used_brutal_strike = self.level < 9
        self.used_gwm = self.level < 4
        self.used_bonus = self.level < 4
        self.used_beserker = self.level < 3
        self.attacks = self.max_attacks

    def turn(self, target):
        self.begin_turn()
        while self.attacks > 0:
            self.attack(target)
            self.attacks -= 1
        # Retaliation
        if self.level >= 10:
            self.attack(target, no_adv=True)

    def attack(self, target, no_adv=False):
        brutal_strike = False
        if not self.used_brutal_strike:
            brutal_strike = True
            self.used_brutal_strike = True
        roll = do_roll(adv=(not brutal_strike and not no_adv))
        if roll == 20:
            self.hit(target, crit=True, brutal_strike=brutal_strike)
            if not self.used_bonus:
                self.attacks += 1
                self.used_bonus = True
        elif roll + self.to_hit >= target.ac:
            self.hit(target, brutal_strike=brutal_strike)
        else:
            target.damage(self.str)

    def hit(self, target, crit=False, brutal_strike=False):
        target.damage(self.weapon() + self.str + self.rage_dmg + self.magic_weapon)
        if not self.used_gwm:
            target.damage(self.prof)
            self.used_gwm = True
        if not self.used_beserker:
            for _ in range(self.rage_dmg):
                target.damage(random.randint(1,6))
            self.used_beserker = True
        if brutal_strike:
            target.damage(self.brutal_strike_dmg())
        if crit:
            target.damage(self.weapon())
            if brutal_strike:
                target.damage(self.brutal_strike_dmg())
            if not self.used_beserker:
                for _ in range(self.rage_dmg):
                    target.damage(random.randint(1,6))
                self.used_beserker = True

    def short_rest(self):
        pass

def simulate(character, level, fights, turns):
    dmg = 0
    for _ in range(fights):
        target = Target(level)
        for _ in range(turns):
            character.turn(target)
            target.turn()
        character.short_rest()
        dmg += target.dmg
    return dmg

def test_dpr(Creator):
    damage = 0
    for _ in range(NUM_SIMS):
        character = Creator(level)
        damage += simulate(character, level, NUM_FIGHTS, NUM_TURNS)
    return damage/(NUM_SIMS*NUM_FIGHTS*NUM_TURNS)


if __name__ == "__main__":
    for level in range(1,21):
        fighter_damage = test_dpr(Fighter)
        monk_damage = test_dpr(Monk)
        barbarian_damage = test_dpr(Barbarian)
        print(f"Fighter {level}: {fighter_damage:0.2f} DPR - Monk {level}: {monk_damage:0.2f} DPR - Barbarian {level}: {barbarian_damage:0.2f}")

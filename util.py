import random
import math

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

def highest_spell_slot(slots, max=9):
    # Finds the highest level spell slot available
    slot = max
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

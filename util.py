import random
import math
from collections import defaultdict

SPELL_SLOTS_ARR = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0
    [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],  # 1
    [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],  # 2
    [0, 4, 2, 0, 0, 0, 0, 0, 0, 0],  # 3
    [0, 4, 3, 0, 0, 0, 0, 0, 0, 0],  # 4
    [0, 4, 3, 2, 0, 0, 0, 0, 0, 0],  # 5
    [0, 4, 3, 3, 0, 0, 0, 0, 0, 0],  # 6
    [0, 4, 3, 3, 1, 0, 0, 0, 0, 0],  # 7
    [0, 4, 3, 3, 2, 0, 0, 0, 0, 0],  # 8
    [0, 4, 3, 3, 3, 1, 0, 0, 0, 0],  # 9
    [0, 4, 3, 3, 3, 2, 0, 0, 0, 0],  # 10
    [0, 4, 3, 3, 3, 2, 1, 0, 0, 0],  # 11
    [0, 4, 3, 3, 3, 2, 1, 0, 0, 0],  # 12
    [0, 4, 3, 3, 3, 2, 1, 1, 0, 0],  # 13
    [0, 4, 3, 3, 3, 2, 1, 1, 0, 0],  # 14
    [0, 4, 3, 3, 3, 2, 1, 1, 1, 0],  # 15
    [0, 4, 3, 3, 3, 2, 1, 1, 1, 0],  # 16
    [0, 4, 3, 3, 3, 2, 1, 1, 1, 1],  # 17
    [0, 4, 3, 3, 3, 3, 1, 1, 1, 1],  # 18
    [0, 4, 3, 3, 3, 3, 2, 1, 1, 1],  # 19
    [0, 4, 3, 3, 3, 3, 2, 2, 1, 1],  # 20
]


def spell_slots(level, half=False):
    if half:
        level = math.ceil(level / 2)
    return SPELL_SLOTS_ARR[level].copy()


def prof_bonus(level):
    return ((level - 1) // 4) + 2


def get_magic_weapon(level):
    if level >= 15:
        return 3
    elif level >= 10:
        return 2
    elif level >= 5:
        return 1
    return 0


def do_roll(adv=False, disadv=False):
    if adv and disadv:
        return random.randint(1, 20)
    elif adv:
        return max(random.randint(1, 20), random.randint(1, 20))
    elif disadv:
        return min(random.randint(1, 20), random.randint(1, 20))
    return random.randint(1, 20)


def roll_dice(num: int, size: int, max_reroll: int = 0) -> float:
    total = 0
    for _ in range(num):
        roll = random.randint(1, size)
        if roll <= max_reroll:
            roll = random.randint(1, size)
        total += roll
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

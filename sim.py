
import random
import math
import csv

from util import prof_bonus
from monk import Monk
from barbarian import Barbarian
from fighter import Fighter
from rogue import Rogue
from wizard import Wizard
from paladin import Paladin
from ranger import Ranger
from cleric import Cleric

NUM_FIGHTS = 2
NUM_TURNS = 6
NUM_SIMS = 500

TARGET_AC = [
    13, # 1
    13, # 2
    13, # 3
    14, # 4
    15, # 5
    15, # 6
    15, # 7
    16, # 8
    16, # 9
    17, # 10
    17, # 11
    17, # 12
    18, # 13
    18, # 14
    18, # 15
    18, # 16
    19, # 17
    19, # 18
    19, # 19
    19, # 20
]


class Target:
    def __init__(self, level):
        self.ac = TARGET_AC[level-1]
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

def test_dpr(character, level):
    damage = 0
    for _ in range(NUM_SIMS):
        damage += simulate(character, level, NUM_FIGHTS, NUM_TURNS)
    return damage/(NUM_SIMS*NUM_FIGHTS*NUM_TURNS)

def write_data(file, data):
    with open(file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

def test_characters(characters):
    data = [["Level","Character","DPR"]]
    for level in range(1,21):
        for [name, Creator] in characters:
            data.append([level,name,test_dpr(Creator(level),level)])
    return data

if __name__ == "__main__":
    data = test_characters([
        ["Monk", Monk], 
        ["Figher", Fighter], 
        ["Barbarian",Barbarian], 
        ["Paladin",Paladin], 
        ["Ranger",Ranger], 
        ["Rogue",Rogue],
        ["Wizard",Wizard],
        ["Cleric",Cleric],
    ])
    write_data("data.csv", data)
    # for level in range(1,21):
    #     lines = []
    #     # lines.append(f"Fighter {level}: {test_dpr(Fighter(level)):0.2f} DPR")
    #     # lines.append(f"Barbarian {level}: {test_dpr(Barbarian(level)):0.2f} DPR")
    #     lines.append(f"Monk {level}: {test_dpr(Monk(level)):0.2f} DPR")
    #     lines.append(f"Paladin {level}: {test_dpr(Paladin(level)):0.2f} DPR")
    #     # lines.append(f"Ranger {level}: {test_dpr(Ranger(level)):0.2f} DPR")
    #     # lines.append(f"Rogue {level}: {test_dpr(Rogue(level)):0.2f} DPR")
    #     lines.append(f"Wizard {level}: {test_dpr(Wizard(level)):0.2f} DPR")
    #     lines.append(f"Cleric {level}: {test_dpr(Cleric(level)):0.2f} DPR")
    #     print(" - ".join(lines))


        # fighter_damage = test_dpr(Fighter(level))
        # fighter_pam_damage = test_dpr(Fighter(level, True))
        # print(f"Fighter (greatsword) {level}: {fighter_damage:0.2f} DPR - Fighter (glaive) {level}: {fighter_pam_damage:0.2f} DPR")

        # barbarian_damage = test_dpr(Barbarian(level))
        # barbarian_pam_damage = test_dpr(Barbarian(level, True))
        # print(f"Barbarian (greatsword) {level}: {barbarian_damage:0.2f} DPR - Barbarian (glaive) {level}: {barbarian_pam_damage:0.2f} DPR")

        # wizard_damage = test_dpr(Wizard(level))
        # print(f"Level {level} -- Wizard: {wizard_damage:0.2f} DPR")
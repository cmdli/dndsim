import csv

from monk import Monk
from barbarian import Barbarian
from fighter import Fighter
from rogue import Rogue
from wizard import Wizard
from paladin import Paladin
from ranger import Ranger
from cleric import Cleric
from target import Target

NUM_FIGHTS = 2
NUM_TURNS = 6
NUM_SIMS = 500


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
    return damage / (NUM_SIMS * NUM_FIGHTS * NUM_TURNS)


def write_data(file, data):
    with open(file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def test_characters(characters):
    data = [["Level", "Character", "DPR"]]
    for level in range(1, 21):
        for [name, Creator] in characters:
            data.append([level, name, test_dpr(Creator(level), level)])
    return data


if __name__ == "__main__":
    data = test_characters(
        [
            ["Monk", Monk],
            ["Figher", Fighter],
            ["Barbarian", Barbarian],
            ["Paladin", Paladin],
            ["Ranger", Ranger],
            ["Rogue", Rogue],
            ["Wizard", Wizard],
            ["Cleric", Cleric],
        ]
    )
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

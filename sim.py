import csv

from monk import Monk
from barbarian import Barbarian
from fighter import (
    Fighter,
    ChampionFighter,
    TrippingFighter,
    PrecisionFighter,
    BattlemasterFighter,
    PrecisionTrippingFighter,
)
from rogue import Rogue
from wizard import Wizard
from paladin import Paladin
from ranger import Ranger
from cleric import Cleric
from target import Target
from log import log

NUM_FIGHTS = 3
NUM_TURNS = 5
NUM_SIMS = 500


def simulate(character, level, fights, rounds):
    dmg = 0
    character.long_rest()
    for _ in range(fights):
        target = Target(level)
        for _ in range(rounds):
            character.turn(target)
            character.enemy_turn(target)
            target.turn()
        character.short_rest()
        target.log_damage_sources()
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
            ["Champion Figher", ChampionFighter],
            # ["Battlemaster Fighter", PrecisionTrippingFighter],
            ["Barbarian", Barbarian],
            ["Paladin", Paladin],
            ["Ranger", Ranger],
            ["Rogue", Rogue],
            ["Wizard", Wizard],
            ["Cleric", Cleric],
        ]
    )
    write_data("data.csv", data)
    log.printReport()

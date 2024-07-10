import csv
import click
from typing import Set

from monk import Monk
from barbarian import Barbarian
from fighter import (
    ChampionFighter,
    PrecisionTrippingFighter,
    TWFFighter,
)
from rogue import AssassinRogue
from wizard import Wizard
from paladin import Paladin
from ranger import GloomstalkerRanger, BeastMasterRanger
from cleric import Cleric
from target import Target
from log import log
from au import AssaultUnit

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


def test_characters(characters, start: int, end: int):
    data = [["Level", "Character", "DPR"]]
    for level in range(start, end + 1):
        for [name, Creator] in characters:
            data.append([level, name, test_dpr(Creator(level), level)])
    return data


CHARACTER_MAPPING = {
    "monk": ["Monk", Monk],
    "champion": ["Champion Fighter", ChampionFighter],
    "battlemaster": ["Battlemaster Fighter", ChampionFighter],
    "barbarian": ["Barbarian", Barbarian],
    "paladin": ["Paladin", Paladin],
    "gloomstalker": ["Gloomstalker Ranger", GloomstalkerRanger],
    "beastmaster": ["Beastmaster Ranger", BeastMasterRanger],
    "rogue": ["Rogue", AssassinRogue],
    "wizard": ["Wizard", Wizard],
    "cleric": ["Cleric", Cleric],
    "au": ["Assault Unit 2 1", AssaultUnit],
}

ALL_CHARACTERS = [
    "monk",
    "champion",
    "barbarian",
    "paladin",
    "beastmaster",
    "rogue",
    "wizard",
    "cleric",
]


def get_characters(names: Set[str]):
    if "all" in names:
        names = set(ALL_CHARACTERS)
    characters = []
    for name in names:
        characters.append(CHARACTER_MAPPING[name.lower()])
    return characters


@click.command()
@click.option("-s", "--start", default=1, help="Start of the level range")
@click.option("-e", "--end", default=20, help="End of the level range")
@click.option("--characters", default="all", help="Characters to test")
def run(start, end, characters):
    characters = get_characters(characters.split(","))
    data = test_characters(
        characters,
        start=start,
        end=end,
    )
    write_data("data.csv", data)
    log.printReport()


if __name__ == "__main__":
    run()

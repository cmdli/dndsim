import csv
import click
from typing import Set, List, Dict

from classes.monk import Monk
from classes.barbarian import Barbarian
from classes.fighter import (
    ChampionFighter,
)
from classes.rogue import AssassinRogue, ArcaneTricksterRogue
from classes.wizard import Wizard
from classes.paladin import Paladin
from classes.ranger import GloomstalkerRanger, BeastMasterRanger
from classes.cleric import Cleric
from classes.au import AssaultUnit
from classes.bard import ValorBard
from sim.target import Target
import sim.character
from util.log import log

NUM_FIGHTS = 3
NUM_TURNS = 5
NUM_SIMS = 500


def simulate(
    character: "sim.character.Character", level: int, fights: int, rounds: int
):
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


class CharacterConfig:
    def __init__(self, name: str, constructor, **kwargs):
        self.name = name
        self.constructor = constructor
        self.args = kwargs


def test_characters(
    characters: List[CharacterConfig], start: int, end: int, extra_args: Dict[str, bool]
):
    data = [["Level", "Character", "DPR"]]
    for level in range(start, end + 1):
        for character in characters:
            args = dict(extra_args)
            args.update(character.args)
            data.append(
                [
                    level,
                    character.name,
                    test_dpr(character.constructor(level, **args), level),
                ]
            )
    return data


CHARACTER_MAPPING = {
    "monk": CharacterConfig("Monk", Monk),
    "champion": CharacterConfig("Champion Fighter", ChampionFighter),
    "battlemaster": CharacterConfig("Battlemaster Fighter", ChampionFighter),
    "barbarian": CharacterConfig("Barbarian", Barbarian),
    "paladin": CharacterConfig("Paladin", Paladin),
    "gloomstalker": CharacterConfig("Gloomstalker Ranger", GloomstalkerRanger),
    "beastmaster": CharacterConfig("Beastmaster Ranger", BeastMasterRanger),
    "rogue": CharacterConfig("Assassin", AssassinRogue),
    "arcane_trickster": CharacterConfig("Arcane Trickster", ArcaneTricksterRogue),
    "wizard": CharacterConfig("Wizard", Wizard),
    "cleric": CharacterConfig("Cleric", Cleric),
    "au": CharacterConfig("Assault Unit 2 1", AssaultUnit),
    "bard": CharacterConfig("Bard", ValorBard),
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


def parse_unknown_args(args: List[str]) -> Dict[str, bool]:
    parsed_args = []
    for arg in args:
        if not arg.startswith("--"):
            raise Exception(f"Invalid argument: {arg}")
        parsed_args.append(arg.strip("-"))
    return {arg: True for arg in parsed_args}


@click.command(
    context_settings=dict(
        ignore_unknown_options=True,
    )
)
@click.option("-s", "--start", default=1, help="Start of the level range")
@click.option("-e", "--end", default=20, help="End of the level range")
@click.option("--characters", default="all", help="Characters to test")
@click.argument("extra_args", nargs=-1, type=click.UNPROCESSED)
def run(start, end, characters, extra_args):
    parsed_extra_args = parse_unknown_args(extra_args)
    characters = get_characters(characters.split(","))
    data = test_characters(
        characters,
        start=start,
        end=end,
        extra_args=parsed_extra_args,
    )
    write_data("data.csv", data)
    log.printReport()


if __name__ == "__main__":
    run()

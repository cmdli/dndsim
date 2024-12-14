import csv
import click
from typing import Set, List, Dict
import random

from util.log import log
from sim import CharacterConfig, Simulation
import configs
import sim.character
import sim.target


NUM_FIGHTS = 3
NUM_TURNS = 5
NUM_SIMS = 1000

# random.seed(1234)


def test_dpr(character: "sim.character.Character", level: int):
    damage = 0
    for _ in range(NUM_SIMS):
        target = sim.target.Target(level)
        simulation = Simulation(character, target, NUM_FIGHTS, NUM_TURNS)
        simulation.run()
        damage += simulation.target.dmg
    return damage / (NUM_SIMS * NUM_FIGHTS * NUM_TURNS)


def write_data(file: str, data):
    with open(file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def test_characters(configs: List[CharacterConfig], start: int, end: int):
    data = [["Level", "Character", "DPR"]]
    for level in range(start, end + 1):
        for config in configs:
            dpr = test_dpr(config.create(level), level)
            data.append([level, config.name, dpr])
    return data


def parse_unknown_args(args: List[str]) -> Dict[str, bool]:
    parsed_args = []
    for arg in args:
        if not arg.startswith("--"):
            raise Exception(f"Invalid argument: {arg}")
        parsed_args.append(arg.strip("-"))
    return {arg: True for arg in parsed_args}


@click.command()
@click.option("-s", "--start", default=1, help="Start of the level range")
@click.option("-e", "--end", default=20, help="End of the level range")
@click.option("--characters", default="all", help="Characters to test")
def run(start, end, characters):
    characters = configs.get_configs(characters.split(","))
    data = test_characters(
        characters,
        start=start,
        end=end,
    )
    write_data("data.csv", data)
    log.printReport()


if __name__ == "__main__":
    run()

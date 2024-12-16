import csv
import multiprocessing.pool
import click
import prettytable
from typing import Set, List, Dict
import random
import multiprocessing

from util.log import log
from sim import CharacterConfig, Simulation
import configs
import sim.character
import sim.target


# random.seed(1234)


class Args:
    def __init__(
        self,
        character: str,
        start_level: int,
        end_level: int,
        iterations: int,
        num_rounds: int,
        num_fights: int,
        debug: bool,
    ) -> None:
        self.character = character
        self.start_level = start_level
        self.end_level = end_level
        self.iterations = iterations
        self.num_rounds = num_rounds
        self.num_fights = num_fights
        self.debug = debug


def test_dpr(
    character: "sim.character.Character",
    level: int,
    num_fights: int,
    num_rounds: int,
    iterations: int,
):
    damage = 0.0
    for _ in range(iterations):
        target = sim.target.Target(level)
        simulation = Simulation(character, target, num_fights, num_rounds)
        simulation.run()
        damage += simulation.target.dmg
    return damage / (num_fights * num_rounds * iterations)


def write_data(file: str, data):
    with open(file, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)


def test_character(args: Args):
    if args.debug:
        log.enable()
    config = configs.get_configs([args.character])[0]
    data = []
    for level in range(args.start_level, args.end_level + 1):
        dpr = test_dpr(
            character=config.create(level),
            level=level,
            num_rounds=args.num_rounds,
            num_fights=args.num_fights,
            iterations=args.iterations,
        )
        data.append([level, config.name, dpr])
    if args.debug:
        log.printReport()
    return data


def test_characters(
    characters: List[str],
    start_level: int,
    end_level: int,
    num_rounds: int,
    num_fights: int,
    iterations: int,
    debug: bool,
):
    data = [["Level", "Character", "DPR"]]
    with multiprocessing.pool.Pool() as p:
        args = [
            Args(
                character=character,
                start_level=start_level,
                end_level=end_level,
                iterations=iterations,
                num_rounds=num_rounds,
                num_fights=num_fights,
                debug=debug,
            )
            for character in characters
        ]
        outputs = p.map(
            test_character,
            args,
        )
        for output in outputs:
            data += output
    return data


def print_data(data):
    table = prettytable.PrettyTable()
    levels = set()
    classes = dict()
    for [level, name, dpr] in data:
        if name not in classes:
            classes[name] = dict()
        classes[name][level] = "{:.2f}".format(dpr)
        levels.add(level)
    levels = sorted(list(levels))
    table.add_column("Level", levels)
    for name in classes:
        table.add_column(name, [classes[name][level] for level in levels])
    print(table)


@click.command()
@click.option("-s", "--start", default=1, help="Start of the level range")
@click.option("-e", "--end", default=20, help="End of the level range")
@click.option("--characters", default="all", help="Characters to test")
@click.option("-o", "--output", default="data.csv", help="Output file")
@click.option("--num_rounds", default=5, help="Number of rounds per fight")
@click.option("--num_fights", default=3, help="Number of fights per long rest")
@click.option("--iterations", default=500, help="Number of simulations to run")
@click.option("--debug", is_flag=True, help="Enable debug metrics")
def run(start, end, characters, output, num_rounds, num_fights, iterations, debug):
    characters = configs.break_out_shortcuts(characters.split(","))
    data = test_characters(
        characters,
        start_level=start,
        end_level=end,
        num_rounds=num_rounds,
        num_fights=num_fights,
        iterations=iterations,
        debug=debug,
    )
    write_data(output, data)
    print_data(data[1:])


if __name__ == "__main__":
    run()

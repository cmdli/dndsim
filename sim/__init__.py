from typing import Callable, Any

import sim.character
import sim.target


class CharacterConfig:
    def __init__(
        self,
        name: str,
        constructor: Callable[[Any], "sim.character.Character"],
        **kwargs
    ):
        self.name = name
        self.constructor = constructor
        self.args = kwargs

    def create(self, level: int) -> "sim.character.Character":
        return self.constructor(level, **self.args)


class Simulation:
    def __init__(
        self,
        character: "sim.character.Character",
        target: "sim.target.Target",
        num_fights: int,
        num_rounds: int,
    ) -> None:
        self.character = character
        self.target = target
        self.num_fights = num_fights
        self.num_rounds = num_rounds

    def run(self) -> None:
        self.character.long_rest()
        self.target.long_rest()
        for _ in range(self.num_fights):
            for _ in range(self.num_rounds):
                self.character.turn(self.target)
                self.character.enemy_turn(self.target)
                self.target.turn()
            self.character.short_rest()
            self.target.log_damage_sources()
        return self.target.dmg

import sim.character
import sim.events


class Attack:
    def __init__(self, name: str) -> None:
        self.name = name

    def to_hit(self, character: "sim.character.Character"):
        raise NotImplementedError()

    def attack_result(
        self, args: "sim.events.AttackResultArgs", character: "sim.character.Character"
    ):
        raise NotImplementedError()

    def min_crit(self):
        return 20

    def is_ranged(self):
        raise NotImplementedError()

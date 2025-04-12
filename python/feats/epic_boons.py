from typing import Literal

import sim.feat


class IrresistibleOffense(sim.feat.Feat):
    def __init__(self, mod: Literal["str", "dex"]) -> None:
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.increase_stat_max(self.mod, 1)
        character.increase_stat(self.mod, 1)

    def attack_result(self, args):
        if args.hits() and args.roll == 20:
            args.add_damage(
                source="IrresistibleOffense", damage=self.character.stat(self.mod)
            )

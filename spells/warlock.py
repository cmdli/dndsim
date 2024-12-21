from typing import Optional

import sim.weapons
import sim.spells
import sim.character
import sim.target

from sim.spells import School
from sim.attack import DamageRoll
from util.util import cantrip_dice


class EldritchBlast(sim.spells.Spell):
    def __init__(self, character_level: int, **kwargs):
        super().__init__("EldritchBlast", 0, school=School.Evocation, **kwargs)
        self.character_level = character_level

    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        if not target:
            return
        for _ in range(character.spells.cantrip_dice()):
            character.spell_attack(
                target=target,
                spell=self,
                damage=DamageRoll(
                    source=self.name,
                    dice=[10],
                ),
                is_ranged=True,
            )

from typing import Optional

import sim.weapons
import sim.spells
import sim.character
import sim.target

from sim.spells import School
from sim.attack import DamageRoll


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
                # TODO: Refactor out the flat damage into the Agonizing Blast feat
                damage=DamageRoll(
                    source=self.name,
                    dice=[10],
                    flat_dmg=self.character.mod(self.character.spells.mod),
                ),
                is_ranged=True,
            )

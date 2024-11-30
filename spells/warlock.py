import sim.weapons
import sim.spells
import sim.character
import sim.target

from typing import Optional


class EldritchBlastBolt(sim.weapons.Weapon):
    def __init__(self, character: "sim.character.Character", **kwargs):
        super().__init__(
            "EldritchBlastBolt", num_dice=1, die=10, override_mod=character.spells.mod
        )


class EldritchBlast(sim.spells.Spell):
    def __init__(self, character_level: int, **kwargs):
        super().__init__("EldritchBlast", 0, **kwargs)
        self.character_level = character_level

    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        if not target:
            return
        weapon = EldritchBlastBolt(character)
        for _ in range(character.spells.cantrip_dice()):
            character.weapon_attack(target, weapon)

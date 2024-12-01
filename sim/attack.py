from typing import Optional

import sim.character
import sim.events
import sim.weapons
import sim.spells


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


class SpellAttack(Attack):
    def __init__(
        self,
        spell: "sim.spells.Spell",
        callback: Optional["sim.events.AttackResultCallback"] = None,
        is_ranged: bool = False,
    ) -> None:
        super().__init__(name=spell.name)
        self.spell = spell
        self.callback = callback
        self.ranged = is_ranged

    def to_hit(self, character: "sim.character.Character"):
        return character.spells.to_hit()

    def attack_result(
        self,
        args: "sim.character.AttackResultArgs",
        character: "sim.character.Character",
    ):
        if self.callback:
            self.callback(args, character)

    def is_ranged(self):
        return self.ranged


class WeaponAttack(Attack):
    def __init__(self, weapon: "sim.weapons.Weapon") -> None:
        super().__init__(weapon.name())
        self.weapon = weapon

    def to_hit(self, character: "sim.character.Character"):
        return self.weapon.to_hit(character)

    def attack_result(
        self,
        args: "sim.events.AttackResultArgs",
        character: "sim.character.Character",
    ):
        self.weapon.attack_result(args, character)

    def min_crit(self):
        return self.weapon.min_crit()

    def is_ranged(self):
        return self.weapon.has_tag("ranged")

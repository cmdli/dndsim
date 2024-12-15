from typing import Optional, List

import sim.character
import sim.events
import sim.weapons
import sim.spellcasting

from util.util import roll_dice


class DamageRoll:
    def __init__(
        self,
        source: str = "Unknown",
        dice: Optional[List[int]] = None,
        num_dice: int = 0,
        die: int = 0,
        flat_dmg: int = 0,
    ) -> None:
        self.source = source
        if dice:
            self.dice = dice
        else:
            self.dice = num_dice * [die]
        self.flat_dmg = flat_dmg
        self.rolls = [roll_dice(1, die) for die in self.dice]

    def total(self):
        return self.flat_dmg + sum(self.rolls)


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
        spell: "sim.spellcasting.Spell",
        damage: Optional[DamageRoll] = None,
        callback: Optional["sim.events.AttackResultCallback"] = None,
        is_ranged: bool = False,
    ) -> None:
        super().__init__(name=spell.name)
        self.spell = spell
        self.callback = callback
        self.ranged = is_ranged
        self.damage = damage

    def to_hit(self, character: "sim.character.Character"):
        return character.spells.to_hit()

    def attack_result(
        self,
        args: "sim.character.AttackResultArgs",
        character: "sim.character.Character",
    ):
        if args.hits() and self.damage:
            dice = 2 * self.damage.dice if args.crit else self.damage.dice
            args.add_damage(self.spell.name, dice=dice, damage=self.damage.flat_dmg)
        if self.callback:
            self.callback(args, character)

    def is_ranged(self):
        return self.ranged


class WeaponAttack(Attack):
    def __init__(self, weapon: "sim.weapons.Weapon") -> None:
        super().__init__(weapon.name)
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

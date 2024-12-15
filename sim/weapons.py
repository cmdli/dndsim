from typing import List, Optional, Literal

from util.taggable import Taggable
from util.util import roll_dice

import sim.events
import sim.spellcasting
import sim.character
import sim.attack

"""
Overlooked things for weapons:
- Versatile (higher die only)
- TwoHanded integration (we dont track hands yet)
- Loading
- Range (Ranged vs Melee is supported)
- Thrown
- Reach
- Ammunition

A few implementation notes:
- Finesse weapons choose the higher of strength or dexterity
"""


WeaponMastery = Literal[
    "Vex",
    "Topple",
    "Slow",
    "Nick",
    "Cleave",
    "Graze",
    "Sap",
]


class Weapon(Taggable):
    def __init__(
        self,
        name: Optional[str] = None,
        num_dice: int = 0,
        die: int = 6,
        damage_type: str = "unknown",
        min_crit: int = 20,
        mastery: Optional[WeaponMastery] = None,
        magic_bonus: int = 0,
        attack_bonus: int = 0,
        dmg_bonus: int = 0,
        tags: Optional[List[str]] = None,
    ) -> None:
        self.name = name or "UnknownWeapon"
        self.num_dice = num_dice
        self.die = die
        self.damage_type = damage_type
        self._min_crit = min_crit
        self.attack_bonus = magic_bonus + attack_bonus
        self.dmg_bonus = magic_bonus + dmg_bonus
        self.mastery = mastery
        if tags:
            self.add_tags(tags)

    def mod(self, character: "sim.character.Character"):
        if self.has_tag("ranged"):
            return "dex"
        elif self.has_tag("finesse") and (
            character.stat("dex") > character.stat("str")
        ):
            return "dex"
        else:
            return "str"

    def to_hit(self, character: "sim.character.Character"):
        mod = self.mod(character)
        return character.prof + character.mod(mod) + self.attack_bonus

    def rolls(self, crit: bool = False):
        num_dice = self.num_dice
        if crit:
            num_dice *= 2
        return [roll_dice(1, self.die) for _ in range(num_dice)]

    def attack_result(
        self, args: "sim.events.AttackResultArgs", character: "sim.character.Character"
    ):
        if args.hits():
            damage = self.dmg_bonus
            args.add_damage(source=self.name, dice=self.num_dice * [self.die])
            if not args.attack.has_tag("light"):
                mod = self.mod(character)
                damage += character.mod(mod)
            args.add_damage(
                source=self.name, dice=self.num_dice * [self.die], damage=damage
            )

    def min_crit(self) -> int:
        return self._min_crit

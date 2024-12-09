from util.util import roll_dice
from typing import List, Optional
import sim.events
import sim.spells
import sim.character
import sim.attack
from util.taggable import Taggable

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

WEAPON_MASTERIES = [
    "vex",
    "topple",
    "slow",
    "nick",
    "cleave",
    "graze",
    "sap",
]


class Weapon(Taggable):
    def __init__(
        self,
        name: Optional[str] = None,
        num_dice: int = 0,
        die: int = 6,
        damage_type: str = "unknown",
        min_crit: int = 20,
        mastery: Optional[str] = None,
        magic_bonus: int = 0,
        attack_bonus: int = 0,
        dmg_bonus: int = 0,
        tags: Optional[List[str]] = None,
        override_mod: Optional[str] = None,
        spell: Optional["sim.spells.Spell"] = None,
    ) -> None:
        self._name = name
        self.num_dice = num_dice
        self.die = die
        self.damage_type = damage_type
        self._min_crit = min_crit
        self.attack_bonus = magic_bonus + attack_bonus
        self.dmg_bonus = magic_bonus + dmg_bonus
        self.override_mod = override_mod
        self.mastery = mastery
        self.spell = spell
        if tags:
            self.add_tags(tags)

    def mod(self, character: "sim.character.Character"):
        if self.override_mod is not None:
            return self.override_mod
        elif self.has_tag("ranged"):
            return "dex"
        elif self.has_tag("finesse") and (character.dex > character.str):
            return "dex"
        else:
            return "str"

    def to_hit(self, character: "sim.character.Character"):
        mod = self.mod(character)
        return character.prof + character.mod(mod) + self.attack_bonus

    def name(self):
        return self._name

    def rolls(self, crit: bool = False):
        num_dice = self.num_dice
        if crit:
            num_dice *= 2
        return [roll_dice(1, self.die) for _ in range(num_dice)]

    def attack_result(
        self, args: "sim.events.AttackResultArgs", character: "sim.character.Character"
    ):
        if args.hits():
            args.add_damage_dice(self.name(), self.num_dice, self.die)
            if not args.attack.has_tag("light") and not args.attack.has_tag("spell"):
                mod = self.mod(character)
                args.add_flat_damage(
                    self.name(),
                    character.mod(mod),
                )
            args.add_flat_damage(self.name(), self.dmg_bonus)

    def min_crit(self) -> int:
        return self._min_crit


class WeaponAttack(sim.attack.Attack):
    def __init__(self, weapon: Weapon) -> None:
        super().__init__(weapon.name())
        self.weapon = weapon

    def to_hit(self, character: "sim.character.Character"):
        return self.weapon.to_hit(character)

    def attack_result(
        self, args: "sim.events.AttackResultArgs", character: "sim.character.Character"
    ):
        self.weapon.attack_result(args, character)

    def min_crit(self):
        return self.weapon.min_crit()

    def is_ranged(self):
        return self.weapon.has_tag("ranged")


class Glaive(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Glaive",
            num_dice=1,
            die=10,
            damage_type="slashing",
            mastery="graze",
            tags=["heavy", "twohanded"],
            **kwargs,
        )


class GlaiveButt(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="GlaiveButt",
            num_dice=1,
            die=4,
            damage_type="bludgeoning",
            mastery="graze",
            tags=["heavy", "twohanded"],
            **kwargs,
        )


class Greatsword(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Greatsword",
            num_dice=2,
            die=6,
            damage_type="slashing",
            mastery="graze",
            tags=["heavy", "twohanded"],
            **kwargs,
        )


class Shortsword(Weapon):
    def __init__(self, name="Shortsword", **kwargs):
        super().__init__(
            name=name,
            num_dice=1,
            die=6,
            damage_type="piercing",
            mastery="vex",
            tags=["finesse", "light"],
            **kwargs,
        )


class Rapier(Weapon):
    def __init__(self, name="Rapier", **kwargs):
        super().__init__(
            name=name,
            num_dice=1,
            die=8,
            damage_type="piercing",
            mastery="vex",
            tags=["finesse"],
            **kwargs,
        )


class Scimitar(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Scimitar",
            num_dice=1,
            die=6,
            damage_type="slashing",
            mastery="nick",
            tags=["finesse", "light"],
            **kwargs,
        )


class Maul(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Maul",
            num_dice=2,
            die=6,
            damage_type="bludgeoning",
            mastery="topple",
            tags=["heavy", "twohanded"],
            **kwargs,
        )


class Quarterstaff(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Quarterstaff",
            num_dice=1,
            die=8,
            damage_type="bludgeoning",
            mastery="topple",
            tags=["twohanded"],
            **kwargs,
        )


class HandCrossbow(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="HandCrossbow",
            num_dice=1,
            die=6,
            damage_type="piercing",
            mastery="vex",
            tags=["ranged", "light"],
            **kwargs,
        )


class Dagger(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Dagger",
            num_dice=1,
            die=4,
            damage_type="piercing",
            mastery="nick",
            tags=["finesse", "light"],
            **kwargs,
        )


class Warhammer(Weapon):
    def __init__(self, **kwargs):
        super().__init__(name="Warhammer", num_dice=1, die=8, damage_type="bludgeoning")

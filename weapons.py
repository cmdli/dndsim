from util import roll_dice
from typing import List

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


class Weapon:
    def __init__(
        self,
        name=None,
        num_dice=0,
        die=6,
        damage_type="unknown",
        min_crit=20,
        mastery: str = None,
        magic_bonus=0,
        attack_bonus=0,
        dmg_bonus=0,
        tags: List[str] = None,
        flat_dmg_bonus: int = None,
        override_to_hit=None,
        override_mod=None,
    ) -> None:
        self.name = name
        self.num_dice = num_dice
        self.die = die
        self.damage_type = damage_type
        self.min_crit = min_crit
        self.attack_bonus = magic_bonus + attack_bonus
        self.dmg_bonus = magic_bonus + dmg_bonus
        self.override_mod = override_mod
        self.override_to_hit = override_to_hit
        self.flat_dmg_bonus = flat_dmg_bonus
        self.mastery = mastery
        self.tags = tags or []

    def damage(self, crit: bool = False, max_reroll: int = None):
        dmg = roll_dice(self.num_dice, self.die, max_reroll=max_reroll)
        if crit:
            dmg += roll_dice(self.num_dice, self.die, max_reroll=max_reroll)
        return dmg

    def rolls(self, crit: bool = False):
        num_dice = self.num_dice
        if crit:
            num_dice *= 2
        return [roll_dice(1, self.die) for _ in range(num_dice)]

    def has_tag(self, tag: str):
        return tag in self.tags


class Glaive(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Glaive",
            num_dice=1,
            die=10,
            damage_type="slashing",
            mastery="graze",
            tags=["heavy"],
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
            tags=["heavy"],
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
            tags=["heavy"],
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
            tags=["heavy"],
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

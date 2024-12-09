import random
from enum import Enum
from typing import Set, List, Optional, TypeAlias, Callable, Any
from collections import defaultdict

from util.util import roll_dice
from util.log import log
from sim.target import Target
import sim.weapons
import sim.spells
import sim.character
import util.taggable
import sim.attack


class AttackArgs(util.taggable.Taggable):
    def __init__(
        self,
        target: Target,
        attack: "sim.attack.Attack",
        weapon: Optional["sim.weapons.Weapon"] = None,
        spell: Optional["sim.spells.Spell"] = None,
        tags: Optional[List[str]] = None,
    ):
        self.target = target
        self.attack = attack
        self.weapon = weapon
        self.spell = spell
        if tags:
            self.add_tags(tags)


class AttackRollArgs:
    def __init__(self, attack: AttackArgs, to_hit: int):
        self.attack = attack
        self.to_hit = to_hit
        self.adv = False
        self.disadv = False
        self.roll1 = random.randint(1, 20)
        self.roll2 = random.randint(1, 20)
        self.situational_bonus = 0

    def reroll(self):
        self.roll1 = random.randint(1, 20)
        self.roll2 = random.randint(1, 20)

    def roll(self):
        if self.adv == self.disadv:
            log.output(lambda: f"Roll: {self.roll1}")
            return self.roll1
        elif self.adv:
            log.output(lambda: f"Roll ADV: {self.roll1}, {self.roll2}")
            return max(self.roll1, self.roll2)
        else:
            log.output(lambda: f"Roll DIS: {self.roll1}, {self.roll2}")
            return min(self.roll1, self.roll2)

    def hits(self):
        return (
            self.roll() + self.to_hit + self.situational_bonus >= self.attack.target.ac
        )


class AttackResultArgs:
    def __init__(
        self,
        attack: AttackArgs,
        hit: bool,
        crit: bool,
        roll: int,
    ):
        self._dice: defaultdict[str, List[int]] = defaultdict(list)
        self._flat_dmg: defaultdict[str, int] = defaultdict(int)
        self.hit = hit
        self.dmg_multiplier = 1.0
        self.attack = attack
        self.crit = crit
        self.roll = roll

    def add_damage(self, source: str, dice: List[int], damage: int = 0):
        if damage:
            self._flat_dmg[source] += damage
        if dice:
            self._dice[source].extend(dice)

    def add_damage_dice(self, source: str, num: int, size: int):
        self.add_damage(source, dice=[size] * num)

    def add_flat_damage(self, source: str, damage: int):
        self.add_damage(source, [], damage=damage)

    def damage_sources(self) -> Set[str]:
        return set(self._dice.keys()).union(set(self._flat_dmg.keys()))

    def hits(self) -> bool:
        return self.hit

    def misses(self) -> bool:
        return not self.hit


AttackResultCallback: TypeAlias = Callable[
    [AttackResultArgs, "sim.character.Character"], Any
]


class EnemySavingThrowArgs:
    def __init__(self) -> None:
        pass


class CastSpellArgs:
    def __init__(self, spell: "sim.spells.Spell") -> None:
        self.spell = spell


class DamageRollArgs:
    def __init__(
        self,
        target: Target,
        dice: List[int],
        flat_dmg: int = 0,
        attack: Optional[AttackArgs] = None,
        spell: Optional["sim.spells.Spell"] = None,
    ) -> None:
        self.target = target
        self.dice = dice or []
        self.rolls = [roll_dice(1, die) for die in self.dice]
        self.flat_dmg = flat_dmg
        self.spell = spell
        self.attack = attack

    def damage_total(self):
        return self.flat_dmg + sum(self.rolls)

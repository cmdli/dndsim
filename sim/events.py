import random
from typing import List, Optional, TypeAlias, Callable, Any

from util.log import log
import sim.target
import sim.weapons
import sim.spells
import sim.character
import util.taggable
import sim.attack


class AttackArgs(util.taggable.Taggable):
    def __init__(
        self,
        target: "sim.target.Target",
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
        if self.adv and self.disadv:
            log.output(lambda: f"Roll: {self.roll1}")
            return self.roll1
        elif self.adv:
            log.output(lambda: f"Roll ADV: {self.roll1}, {self.roll2}")
            return max(self.roll1, self.roll2)
        elif self.disadv:
            log.output(lambda: f"Roll DIS: {self.roll1}, {self.roll2}")
            return min(self.roll1, self.roll2)
        else:
            return self.roll1

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
        self.damage_rolls: List["sim.attack.DamageRoll"] = []
        self.hit = hit
        self.dmg_multiplier = 1.0
        self.attack = attack
        self.crit = crit
        self.roll = roll

    def add_damage(
        self,
        source: str,
        dice: Optional[List[int]] = None,
        damage: int = 0,
    ):
        dice = dice or []
        self.damage_rolls.append(
            sim.attack.DamageRoll(source=source, dice=dice, flat_dmg=damage)
        )

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
        target: "sim.target.Target",
        damage: sim.attack.DamageRoll,
        attack: Optional[AttackArgs] = None,
        spell: Optional["sim.spells.Spell"] = None,
    ) -> None:
        self.target = target
        self.damage = damage
        self.spell = spell
        self.attack = attack

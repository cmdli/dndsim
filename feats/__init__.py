from typing import List, Literal

from util.util import roll_dice
from util.log import log

import sim.character
import sim.feat
import sim.weapons
import sim.target


class PolearmMaster(sim.feat.Feat):
    def __init__(self, weapon: "sim.weapons.Weapon"):
        # NOTE: Weapon must be of the 'butt' variety (e.g. uses a d4 for damage)
        self.weapon = weapon
        self.enabled = False

    def apply(self, character):
        super().apply(character)
        character.increase_stat("str", 1)

    def begin_turn(self, target):
        self.enabled = False

    def attack(self, args):
        weapon = args.weapon
        if weapon and weapon.has_tag("reach") and weapon.has_tag("heavy"):
            self.enabled = True

    def end_turn(self, target):
        if self.enabled and self.character.use_bonus("PolearmMaster"):
            self.character.weapon_attack(target, self.weapon, tags="PolearmMaster")


class GreatWeaponMaster(sim.feat.Feat):
    def __init__(self, weapon: "sim.weapons.Weapon"):
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.increase_stat("str", 1)

    def attack_result(self, args):
        if args.misses():
            return
        if args.attack.weapon.has_tag("heavy"):
            args.add_damage(source="GreatWeaponMaster", damage=self.character.prof)
        if args.crit and self.character.use_bonus("GreatWeaponMaster"):
            self.character.weapon_attack(args.attack.target, self.weapon)


class ElvenAccuracy(sim.feat.Feat):
    def __init__(self, mod: "sim.Stat"):
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.increase_stat(self.mod, 1)

    def attack_roll(self, args):
        if args.adv:
            roll = roll_dice(1, 20)
            if args.roll1 < args.roll2 and args.roll1 < roll:
                args.roll1 = roll
            elif args.roll2 < roll:
                args.roll2 = roll


class Archery(sim.feat.Feat):
    def attack_roll(self, args):
        weapon = args.attack.weapon
        if weapon and weapon.has_tag("ranged"):
            args.situational_bonus += 2


class TwoWeaponFighting(sim.feat.Feat):
    def attack_roll(self, args):
        if args.attack.has_tag("light"):
            args.attack.remove_tag("light")


class GreatWeaponFighting(sim.feat.Feat):
    def damage_roll(self, args):
        weapon = args.attack.weapon if args.attack and args.attack.weapon else None
        if weapon and weapon.has_tag("twohanded"):
            for i in range(len(args.damage.rolls)):
                if args.damage.rolls[i] == 1 or args.damage.rolls[i] == 2:
                    args.damage.rolls[i] = 3


class CrossbowExpert(sim.feat.Feat):
    def __init__(self, weapon: "sim.weapons.Weapon") -> None:
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.increase_stat("dex", 1)

    def attack(self, args):
        if args.has_tag("light"):
            args.remove_tag("light")


class ASI(sim.feat.Feat):
    def __init__(self, stat_increases: List["sim.Stat"] = []):
        self.stat_increases = stat_increases

    def apply(self, character: "sim.character.Character"):
        super().apply(character)
        increase = 2 if len(self.stat_increases) == 1 else 1
        for stat in self.stat_increases:
            character.increase_stat(stat, increase)


class AttackAction(sim.feat.Feat):
    def __init__(self, attacks, nick_attacks=[]):
        self.base_attacks = attacks
        self.nick_attacks = nick_attacks

    def action(self, target):
        for weapon in self.base_attacks:
            self.character.weapon_attack(target, weapon, tags=["main_action"])
        for weapon in self.nick_attacks:
            self.character.weapon_attack(target, weapon, tags=["main_action", "light"])


class BoomingBlade(sim.feat.Feat):
    def __init__(
        self, character: "sim.character.Character", weapon: "sim.weapons.Weapon"
    ):
        self.weapon = weapon
        self.character = character

    def action(self, target):
        self.character.weapon_attack(
            target, self.weapon, tags=["main_action", "booming_blade"]
        )

    def attack_result(self, args):
        if args.misses() or not args.attack.has_tag("booming_blade"):
            return
        if self.character.level >= 17:
            extra_dice = 3
        elif self.character.level >= 11:
            extra_dice = 2
        elif self.character.level >= 5:
            extra_dice = 1
        else:
            return
        args.add_damage(source="BoomingBlade", dice=extra_dice * [8])


class LightWeaponBonusAttack(sim.feat.Feat):
    def __init__(self, weapon: "sim.weapons.Weapon") -> None:
        self.weapon = weapon
        self.enabled = False

    def begin_turn(self, target):
        self.enabled = False

    def attack(self, args):
        if args.weapon is not None and args.weapon.has_tag("light"):
            self.enabled = True

    def end_turn(self, target):
        if self.enabled and self.character.use_bonus("LightWeaponBonusAttack"):
            self.character.weapon_attack(target, self.weapon, tags=["light"])


class Vex(sim.feat.Feat):
    def __init__(self) -> None:
        self.vexing = False

    def short_rest(self):
        self.vexing = False

    def attack_roll(self, args):
        if self.vexing:
            args.adv = True
            self.vexing = False

    def attack_result(self, args):
        weapon = args.attack.weapon
        if (
            args.hits()
            and weapon
            and weapon.mastery == "Vex"
            and "Vex" in self.character.masteries
        ):
            self.vexing = True


class Topple(sim.feat.Feat):
    def attack_result(self, args):
        weapon = args.attack.weapon
        if not weapon or args.misses():
            return
        target = args.attack.target
        if weapon.mastery == "Topple" and "Topple" in self.character.masteries:
            mod = weapon.mod(self.character)
            if not target.save(self.character.dc(mod)):
                target.knock_prone()


class Graze(sim.feat.Feat):
    def attack_result(self, args):
        weapon = args.attack.weapon
        if not weapon or not args.misses():
            return
        if weapon.mastery == "Graze" and "Graze" in self.character.masteries:
            mod = weapon.mod(self.character)
            args.attack.target.damage_source("Graze", self.character.mod(mod))


class WeaponMasteries(sim.feat.Feat):
    def __init__(self, masteries: List["sim.weapons.WeaponMastery"]) -> None:
        self.masteries = masteries

    def apply(self, character):
        super().apply(character)
        character.masteries.update(self.masteries)


class IrresistibleOffense(sim.feat.Feat):
    def __init__(self, mod: Literal["str", "dex"]) -> None:
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.increase_stat_max(self.mod, 1)
        character.increase_stat(self.mod, 1)

    def attack_result(self, args):
        if args.hits() and args.roll == 20:
            args.add_damage(
                source="IrresistibleOffense", damage=self.character.stat(self.mod)
            )


class WeaponMaster(sim.feat.Feat):
    def __init__(
        self, mod: Literal["str", "dex"], mastery: "sim.weapons.WeaponMastery"
    ) -> None:
        self.mod = mod
        self.mastery = mastery

    def apply(self, character):
        super().apply(character)
        character.increase_stat(self.mod, 1)
        character.masteries.add(self.mastery)


class DualWielder(sim.feat.Feat):
    def __init__(
        self, mod: Literal["str", "dex"], weapon: "sim.weapons.Weapon"
    ) -> None:
        self.mod = mod
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.increase_stat(self.mod, 1)

    def after_action(self, target):
        if self.character.use_bonus("DualWielder"):
            self.character.weapon_attack(target, self.weapon, tags=["light"])


class SavageAttacker(sim.feat.Feat):
    def __init__(self) -> None:
        self.used = False

    def begin_turn(self, target):
        self.used = False

    def damage_roll(self, args):
        if self.used or not args.attack.weapon:
            return
        self.used = True
        new_rolls = [roll_dice(1, die) for die in args.damage.dice]
        if sum(new_rolls) > sum(args.damage.rolls):
            args.damage.rolls = new_rolls


class Piercer(sim.feat.Feat):
    def __init__(self, mod: Literal["str", "dex"]) -> None:
        self.mod = mod
        self.used = False

    def apply(self, character):
        super().apply(character)
        character.increase_stat(self.mod, 1)

    def begin_turn(self, target):
        self.used = False

    def damage_roll(self, args):
        if (
            args.attack.weapon is not None
            and not self.used
            and args.attack.weapon.damage_type == "piercing"
        ):
            self.used = True
            lowest = min(args.damage.rolls)
            for i in range(len(args.damage.rolls)):
                if args.damage.rolls[i] == lowest:
                    args.damage.rolls[i] = roll_dice(1, args.damage.dice[i])
                    break

    def attack_result(self, args):
        if args.hits() and args.crit and args.attack.weapon.damage_type == "piercing":
            args.add_damage(source="PiercerCrit", dice=[args.attack.weapon.die])

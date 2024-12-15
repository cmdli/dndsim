from typing import List

from util.util import roll_dice
from util.log import log

import sim.character
import sim.feat
import sim.weapons
import sim.target


class PolearmMaster(sim.feat.Feat):
    def __init__(self, weapon: "sim.weapons.Weapon"):
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.increase_stat("str", 1)

    def begin_turn(self, target):
        self.used = False

    def end_turn(self, target):
        if not self.used and self.character.use_bonus("PAM"):
            self.used = True
            self.character.weapon_attack(target, self.weapon)


class GreatWeaponMaster(sim.feat.Feat):
    def __init__(self, weapon: "sim.weapons.Weapon"):
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.increase_stat("str", 1)

    def begin_turn(self, target):
        self.bonus_attack_enabled = False

    def attack_result(self, args):
        if args.misses():
            return
        if args.attack.weapon.has_tag("heavy"):
            args.add_damage(source="GreatWeaponMaster", damage=self.character.prof)
        if args.crit:
            self.bonus_attack_enabled = True

    def after_action(self, target):
        if self.bonus_attack_enabled and self.character.use_bonus("GreatWeaponMaster"):
            self.character.weapon_attack(target, self.weapon)


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
        attack = args.attack
        if attack:
            weapon = attack.weapon
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

    def begin_turn(self, target):
        self.used_attack = False

    def attack(self, args):
        self.used_attack = True

    def end_turn(self, target):
        if self.used_attack and self.character.use_bonus("CrossbowExpert"):
            self.character.weapon_attack(target, self.weapon)


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

    def end_turn(self, target):
        if self.character.use_bonus("LightWeaponBonusAttack"):
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
            and weapon.mastery == "vex"
            and self.character.has_mastery("vex")
        ):
            self.vexing = True


class Topple(sim.feat.Feat):
    def attack_result(self, args):
        weapon = args.attack.weapon
        if not weapon or args.misses():
            return
        target = args.attack.target
        if weapon.mastery == "topple" and self.character.has_mastery("topple"):
            mod = weapon.mod(self.character)
            if not target.save(self.character.dc(mod)):
                target.knock_prone()


class Graze(sim.feat.Feat):
    def attack_result(self, args):
        weapon = args.attack.weapon
        if not weapon or not args.misses():
            return
        if weapon.mastery == "graze" and self.character.has_mastery("graze"):
            mod = weapon.mod(self.character)
            args.attack.target.damage_source("Graze", self.character.mod(mod))


class WeaponMasteries(sim.feat.Feat):
    def __init__(self, masteries: List[str]) -> None:
        self.masteries = masteries

    def apply(self, character):
        super().apply(character)
        character.add_masteries(self.masteries)


class IrresistibleOffense(sim.feat.Feat):
    def __init__(self, mod: "sim.Stat") -> None:
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.increase_stat_max(self.mod, 1)
        character.increase_stat(self.mod, 1)

    def attack_result(self, args):
        if args.hits() and args.roll == 20:
            args.add_damage(source="IrresistibleOffense", damage=self.character.str)


class WeaponMaster(sim.feat.Feat):
    def __init__(self, mod: "sim.Stat") -> None:
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.increase_stat(self.mod, 1)


class DualWielder(sim.feat.Feat):
    def __init__(self, mod: "sim.Stat", weapon: "sim.weapons.Weapon") -> None:
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
        if self.used:
            return
        self.used = True
        new_rolls = [roll_dice(1, die) for die in args.damage.dice]
        if sum(new_rolls) > sum(args.damage.rolls):
            args.damage.rolls = new_rolls


class Piercer(sim.feat.Feat):
    def __init__(self, mod: "sim.Stat") -> None:
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.increase_stat(self.mod, 1)

    def attack_result(self, args):
        if args.hits() and args.crit and args.attack.weapon.damage_type == "piercing":
            args.add_damage(source="PiercerCrit", dice=[args.attack.weapon.die])

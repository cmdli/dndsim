from sim.events import HitArgs, AttackRollArgs, AttackArgs, MissArgs, WeaponRollArgs
from util.util import roll_dice
from sim.target import Target
from sim.weapons import Weapon
from util.log import log
from typing import List

EVENT_NAMES = set(
    [
        "begin_turn",
        "before_action",
        "action",
        "after_action",
        "before_attack",
        "attack",
        "roll_attack",
        "hit",
        "miss",
        "end_turn",
        "enemy_turn",
        "short_rest",
        "long_rest",
        "weapon_roll",
    ]
)


class Feat:
    def apply(self, character):
        self.character = character

    def events(self):
        global EVENT_NAMES
        return [name for name in self.__dir__() if name in EVENT_NAMES]


class PolearmMaster(Feat):
    def __init__(self, weapon):
        self.name = "PolearmMaster"
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.str += 1

    def begin_turn(self, target):
        self.used = False

    def end_turn(self, target):
        if not self.used and self.character.use_bonus("PAM"):
            self.used = True
            self.character.attack(target, self.weapon)


class GreatWeaponMaster(Feat):
    def __init__(self, weapon: Weapon):
        self.name = "GreatWeaponMaster"
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.str += 1

    def begin_turn(self, target):
        self.bonus_attack_enabled = False

    def hit(self, args: HitArgs):
        if args.attack.weapon.has_tag("heavy"):
            args.add_damage("GreatWeaponMaster", self.character.prof)
        if args.crit:
            self.bonus_attack_enabled = True

    def after_action(self, target: Target):
        if self.bonus_attack_enabled and self.character.use_bonus("GreatWeaponMaster"):
            self.character.attack(target, self.weapon)


class ElvenAccuracy(Feat):
    def __init__(self, mod: str):
        self.name = "ElvenAccuracy"
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.__setattr__(self.mod, character.__getattribute__(self.mod) + 1)

    def roll_attack(self, args: AttackRollArgs):
        if args.adv:
            roll = roll_dice(1, 20)
            if args.roll1 < args.roll2 and args.roll1 < roll:
                args.roll1 = roll
            elif args.roll2 < roll:
                args.roll2 = roll


class Archery(Feat):
    def __init__(self) -> None:
        self.name = "Archery"

    def roll_attack(self, args: AttackRollArgs):
        if args.attack.weapon.has_tag("ranged"):
            args.situational_bonus += 2


class DualWielder(Feat):
    def __init__(self, weapon: Weapon):
        self.name = "DualWielder"
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.dex += 1

    def after_actions(self, target: Target):
        if self.character.use_bonus("DualWielder"):
            self.character.attack(target, self.weapon)


class TwoWeaponFighting(Feat):
    def __init__(self) -> None:
        self.name = "TwoWeaponFighting"

    def roll_attack(self, args: AttackRollArgs):
        if args.attack.has_tag("light"):
            args.attack.remove_tag("light")


class GreatWeaponFighting(Feat):
    def __init__(self) -> None:
        self.name = "GreatWeaponFighting"

    def weapon_roll(self, args: WeaponRollArgs):
        for i in range(len(args.rolls)):
            if args.rolls[i] == 1 or args.rolls[i] == 2:
                args.rolls[i] = 3


class CrossbowExpert(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.name = "CrossbowExpert"
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.dex += 1

    def begin_turn(self, target: Target):
        self.used_attack = False

    def attack(self, args: AttackArgs):
        self.used_attack = True

    def end_turn(self, target):
        if self.used_attack and self.character.use_bonus("CrossbowExpert"):
            log.record("bonus attack", 1)
            self.character.attack(target, self.weapon)


class ASI(Feat):
    def __init__(self, stat_increases=[]):
        self.name = "ASI"
        self.stat_increases = stat_increases

    def apply(self, character):
        super().apply(character)
        for [stat, increase] in self.stat_increases:
            character.__setattr__(stat, character.__getattribute__(stat) + increase)


class AttackAction(Feat):
    def __init__(self, attacks, nick_attacks=[]):
        self.name = "AttackAction"
        self.base_attacks = attacks
        self.nick_attacks = nick_attacks

    def action(self, target):
        for weapon in self.base_attacks:
            self.character.attack(target, weapon, tags=["main_action"])
        for weapon in self.nick_attacks:
            self.character.attack(target, weapon, tags=["main_action", "light"])


class BoomingBlade(Feat):
    def __init__(self, character, weapon: Weapon):
        self.name = "BoomingBladeAction"
        self.weapon = weapon
        self.character = character

    def action(self, target):
        self.character.attack(
            target, self.weapon, tags=["main_action", "booming_blade"]
        )

    def hit(self, args: HitArgs):
        if not args.attack.has_tag("booming_blade"):
            return
        if self.character.level >= 17:
            extra_dice = 3
        elif self.character.level >= 11:
            extra_dice = 2
        elif self.character.level >= 5:
            extra_dice = 1
        else:
            return
        if args.crit:
            extra_dice *= 2
        args.add_damage("BoomingBlade", roll_dice(extra_dice, 8))


class LightWeaponBonusAttack(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.name = "LightWeaponBonusAttack"
        self.weapon = weapon

    def end_turn(self, target):
        if self.character.use_bonus("LightWeaponBonusAttack"):
            self.character.attack(target, self.weapon, tags=["light"])


class Vex(Feat):
    def __init__(self) -> None:
        self.name = "Vex"
        self.vexing = False

    def short_rest(self):
        self.vexing = False

    def roll_attack(self, args: AttackRollArgs):
        if self.vexing:
            args.adv = True
            self.vexing = False

    def hit(self, args: HitArgs):
        if args.attack.weapon.mastery == "vex" and self.character.has_mastery("vex"):
            self.vexing = True


class Topple(Feat):
    def __init__(self) -> None:
        self.name = "Topple"

    def hit(self, args: HitArgs):
        weapon = args.attack.weapon
        target = args.attack.target
        if weapon.mastery == "topple" and self.character.has_mastery("topple"):
            if not target.save(self.character.dc(args.attack.mod)):
                log.output(lambda: "Knocked prone")
                target.prone = True


class Graze(Feat):
    def __init__(self) -> None:
        self.name = "Graze"

    def miss(self, args: MissArgs):
        if args.attack.weapon.mastery == "graze" and self.character.has_mastery(
            "graze"
        ):
            args.attack.target.damage_source(
                "Graze", self.character.mod(args.attack.mod)
            )


class WeaponMasteries(Feat):
    def __init__(self, masteries: List[str]) -> None:
        self.name = "WeaponMasteries"
        self.masteries = masteries

    def apply(self, character):
        super().apply(character)
        character.add_masteries(self.masteries)


class IrresistibleOffense(Feat):
    def __init__(self, mod: str) -> None:
        self.name = "IrresistibleOffense"
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.__setattr__(self.mod, character.__getattribute__(self.mod) + 1)

    def hit(self, args: HitArgs):
        if args.roll == 20:
            args.add_damage("IrresistibleOffense", self.character.str)


class CombatProwess(Feat):
    def __init__(self) -> None:
        self.name = "CombatProwess"

    def apply(self, character):
        super().apply(character)
        character.str += 1

    def begin_turn(self, target: Target):
        self.used = False

    def miss(self, args: MissArgs):
        if not self.used:
            self.used = True
            self.character.hit(args.attack)


class WeaponMaster(Feat):
    def __init__(self, mod: str) -> None:
        self.name = "WeaponMaster"
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.__setattr__(self.mod, character.__getattribute__(self.mod) + 1)


class DualWielder(Feat):
    def __init__(self, mod: str) -> None:
        self.name = "DualWielder"
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.__setattr__(self.mod, character.__getattribute__(self.mod) + 1)


class SavageAttacker(Feat):
    def __init__(self) -> None:
        self.name = "SavageAttacker"
        self.used = False

    def begin_turn(self, target: Target):
        self.used = False

    def weapon_roll(self, args: WeaponRollArgs):
        if self.used:
            return
        self.used = True
        new_rolls = args.weapon.rolls(crit=args.crit)
        if sum(new_rolls) > sum(args.rolls):
            args.rolls = new_rolls


class Piercer(Feat):
    def __init__(self, mod: str) -> None:
        self.name = "Piercer"
        self.mod = mod

    def apply(self, character):
        super().apply(character)
        character.__setattr__(self.mod, character.__getattribute__(self.mod) + 1)

    def hit(self, args: HitArgs):
        if args.crit and args.attack.weapon.damage_type == "piercing":
            args.add_damage("PiercerCrit", roll_dice(1, args.attack.weapon.die))

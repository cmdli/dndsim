from events import HitArgs, AttackRollArgs, AttackArgs, MissArgs
from util import roll_dice, spell_slots
from target import Target
from weapons import Weapon
from log import log


class Feat:
    def apply(self, character):
        self.character = character

    def begin_turn(self, target: Target):
        pass

    def action(self, target: Target):
        pass

    def before_attack(self):
        pass

    def attack(self, args: AttackArgs):
        pass

    def roll_attack(self, args: AttackRollArgs):
        pass

    def hit(self, args: HitArgs):
        pass

    def miss(self, args: MissArgs):
        pass

    def end_turn(self, target):
        pass

    def enemy_turn(self, target):
        pass

    def short_rest(self):
        pass

    def long_rest(self):
        pass


class PolearmMaster(Feat):
    def __init__(self, weapon):
        self.name = "PolearmMaster"
        self.weapon = weapon

    def apply(self, character):
        self.character = character
        character.str += 1

    def begin_turn(self, target):
        self.used = False

    def end_turn(self, target):
        if not self.used and self.character.use_bonus("PAM"):
            self.used = True
            self.character.attack(target, self.weapon)


class GreatWeaponMaster(Feat):
    def __init__(self):
        self.name = "GreatWeaponMaster"

    def apply(self, character):
        character.str += 1
        self.character = character

    def begin_turn(self, target):
        self.used_dmg = False
        self.bonus_attack_enabled = False

    def hit(self, args):
        if not self.used_dmg:
            self.used_dmg = True
            args.add_damage("GreatWeaponMaster", self.character.prof)
        if args.crit and self.character.use_bonus("GWM"):
            self.bonus_attack_enabled = True
            self.character.attack(args.target, args.weapon)


class ASI(Feat):
    def __init__(self, stat_increases=[]):
        self.name = "ASI"
        self.stat_increases = stat_increases

    def apply(self, character):
        for [stat, increase] in self.stat_increases:
            new_stat = min(20, character.__getattribute__(stat) + increase)
            character.__setattr__(stat, new_stat)


class AttackAction(Feat):
    def __init__(self, attacks):
        self.name = "AttackAction"
        self.base_attacks = attacks

    def apply(self, character):
        self.character = character

    def action(self, target):
        for weapon in self.base_attacks:
            self.character.attack(
                target,
                weapon,
                main_action=True,
            )


class Attack(Feat):
    def __init__(self):
        self.name = "Attack"

    def apply(self, character):
        self.character = character

    def roll_attack(self, args):
        if args.target.vexed:
            args.adv = True
            args.target.vexed = False
        if args.target.stunned:
            args.adv = True
        if args.target.prone:
            if args.weapon.ranged:
                args.disadv = True
            else:
                args.adv = True

    def attack(self, args):
        log.record(f"Attack:{args.weapon.name}", 1)
        self.character.before_attack()
        to_hit = (
            self.character.prof
            + self.character.mod(args.weapon.mod)
            + args.weapon.bonus
        )
        result = self.character.roll_attack(args.target, args.weapon, to_hit)
        roll = result.roll()
        crit = False
        if roll >= args.weapon.min_crit:
            crit = True
        if roll + to_hit + result.situational_bonus >= args.target.ac:
            self.character.hit(args.target, args.weapon, crit=crit, attack_args=args)
        else:
            self.character.miss(args.target, args.weapon)


class EquipWeapon(Feat):
    def __init__(
        self,
        weapon=None,
        savage_attacker=False,
        max_reroll=0,
    ):
        self.name = weapon.name
        self.weapon = weapon
        self.savage_attacker = savage_attacker
        self.max_reroll = max_reroll

    def apply(self, character):
        self.character = character

    def begin_turn(self, target):
        self.used_savage_attacker = False

    def weapon_dmg(self):
        return roll_dice(
            self.weapon.num_dice, self.weapon.die, max_reroll=self.max_reroll
        )

    def damage(self, crit=False):
        dmg = self.weapon_dmg()
        if crit:
            dmg += self.weapon_dmg()
        return dmg

    def hit(self, args):
        if args.weapon.name != self.weapon.name:
            return
        log.record(f"Hit:{args.weapon.name}", 1)
        dmg = self.damage(crit=args.crit)
        if not self.used_savage_attacker and self.savage_attacker:
            self.used_savage_attacker = True
            dmg2 = self.damage(crit=args.crit)
            dmg = max(dmg, dmg2)
        args.add_damage(f"Weapon:{args.weapon.name}", dmg)
        args.add_damage(
            f"WeaponMod:{args.weapon.name}", self.character.mod(self.weapon.mod)
        )
        args.add_damage(f"WeaponBonus:{args.weapon.name}", self.weapon.bonus)
        if self.weapon.vex:
            args.target.vexed = True
        if self.weapon.topple:
            if not args.target.save(self.character.dc(args.weapon.mod)):
                args.target.prone = True

    def miss(self, args):
        if args.weapon.name != self.weapon.name:
            return
        if self.weapon.graze:
            args.target.damage_source("Graze", self.character.mod(self.weapon.mod))


class SpellSlots(Feat):
    def __init__(self, level, half=False) -> None:
        self.name = "SpellSlots"
        self.level = level
        self.half = half

    def apply(self, character):
        self.character = character

    def long_rest(self):
        self.character.slots = spell_slots(self.level, half=self.half)

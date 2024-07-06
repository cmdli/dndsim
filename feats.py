from events import HitArgs, AttackRollArgs, AttackArgs, MissArgs
from util import roll_dice
from target import Target
from weapons import Weapon


class Feat:
    def apply(self, character):
        pass

    def begin_turn(self, target: Target):
        pass

    def action(self, target: Target):
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
        if not self.used and not self.character.used_bonus:
            self.used = True
            self.character.used_bonus = True
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
            args.dmg += self.character.prof
        if args.crit and not self.character.used_bonus:
            self.bonus_attack_enabled = True
            self.character.used_bonus = True
            self.character.attack(args.target, args.weapon)


class ASI(Feat):
    def __init__(self, stat_increases=[]):
        self.name = "ASI"
        self.stat_increases = stat_increases

    def apply(self, character):
        for [stat, increase] in self.stat_increases:
            character.__setattr__(stat, character.__getattribute__(stat) + increase)


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

    def attack(self, args):
        roll = self.character.roll_attack(args.target)
        to_hit = (
            self.character.prof
            + self.character.mod(args.weapon.mod)
            + args.weapon.bonus
        )
        crit = False
        if roll >= args.weapon.min_crit:
            crit = True
        if roll + to_hit >= args.target.ac:
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
        dmg = self.damage(crit=args.crit)
        if not self.used_savage_attacker and self.savage_attacker:
            self.used_savage_attacker = True
            dmg2 = self.damage(crit=args.crit)
            dmg = max(dmg, dmg2)
        args.dmg += dmg + self.character.mod(self.weapon.mod) + self.weapon.bonus
        if self.weapon.vex:
            args.target.vexed = True

    def miss(self, args):
        if args.weapon.name != self.weapon.name:
            return
        if self.weapon.graze:
            args.target.damage(self.character.mod(self.weapon.mod))

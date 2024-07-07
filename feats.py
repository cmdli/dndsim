from events import HitArgs, AttackRollArgs, AttackArgs, MissArgs
from util import roll_dice, spell_slots, highest_spell_slot
from target import Target
from weapons import Weapon
from log import log
from spells import Spell


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
        super().apply(character)
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
        super().apply(character)
        character.str += 1

    def begin_turn(self, target):
        self.used_dmg = False
        self.bonus_attack_enabled = False

    def hit(self, args):
        if not self.used_dmg:
            self.used_dmg = True
            args.add_damage("GreatWeaponMaster", self.character.prof)
        if args.crit and self.character.use_bonus("GWM"):
            self.bonus_attack_enabled = True
            self.character.attack(args.attack.target, args.attack.weapon)


class Archery(Feat):
    def __init__(self) -> None:
        self.name = "Archery"

    def roll_attack(self, args: AttackRollArgs):
        if args.attack.weapon.ranged:
            args.situational_bonus += 2


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
            new_stat = min(20, character.__getattribute__(stat) + increase)
            character.__setattr__(stat, new_stat)


class AttackAction(Feat):
    def __init__(self, attacks):
        self.name = "AttackAction"
        self.base_attacks = attacks

    def action(self, target):
        for weapon in self.base_attacks:
            self.character.attack(target, weapon, tags=["main_action"])


class Attack(Feat):
    def __init__(self):
        self.name = "Attack"

    def roll_attack(self, args):
        if args.attack.target.stunned:
            args.adv = True
        if args.attack.target.prone:
            if args.attack.weapon.ranged:
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
        result = self.character.roll_attack(attack=args, to_hit=to_hit)
        roll = result.roll()
        crit = False
        if roll >= args.weapon.min_crit:
            crit = True
        if roll + to_hit + result.situational_bonus >= args.target.ac:
            self.character.hit(attack=args, crit=crit)
        else:
            self.character.miss(attack=args)


class EquipWeapon(Feat):
    def __init__(
        self,
        weapon: Weapon = None,
        savage_attacker: bool = False,
        max_reroll: int = 0,
    ):
        self.name = weapon.name
        self.weapon = weapon
        self.savage_attacker = savage_attacker
        self.max_reroll = max_reroll

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
        target = args.attack.target
        weapon = args.attack.weapon
        if weapon.name != self.weapon.name:
            return
        log.record(f"Hit:{weapon.name}", 1)
        dmg = self.damage(crit=args.crit)
        if not self.used_savage_attacker and self.savage_attacker:
            self.used_savage_attacker = True
            dmg2 = self.damage(crit=args.crit)
            dmg = max(dmg, dmg2)
        total_dmg = dmg + weapon.bonus
        if not args.attack.has_tag("light"):
            total_dmg += args.attack.character.mod(weapon.mod)
        args.add_damage(f"Weapon:{weapon.name}", total_dmg)
        if weapon.topple:
            if not target.save(args.attack.character.dc(weapon.mod)):
                target.prone = True

    def miss(self, args):
        if args.attack.weapon.name != self.weapon.name:
            return
        if self.weapon.graze:
            args.attack.target.damage_source(
                "Graze", args.attack.character.mod(self.weapon.mod)
            )


class Spellcasting(Feat):
    def __init__(self, level, half=False) -> None:
        self.name = "Spellcasting"
        self.level = level
        self.half = half
        self.concentration: Spell = None

    def long_rest(self):
        self.slots = spell_slots(self.level, half=self.half)

    def short_rest(self):
        if self.concentration is not None:
            self.concentration.end()
            self.concentration = None

    def highest_slot(self):
        return highest_spell_slot(self.slots)

    def cast(self, spell: Spell):
        self.slots[spell.slot] -= 1
        if spell.concentration:
            self.concentration = spell
        spell.begin(self.character)

    def concentrating_on(self, name: str):
        return self.concentration is not None and self.concentration.name is name

    def is_concentrating(self):
        return self.concentration is not None


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
        if args.attack.weapon.vex:
            self.vexing = True

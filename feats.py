from events import HitArgs, AttackRollArgs, AttackArgs, MissArgs
from util import roll_dice, spell_slots, highest_spell_slot, lowest_spell_slot
from target import Target
from weapons import Weapon
from log import log
from spells import Spell

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
        self.used_dmg = False
        self.bonus_attack_enabled = False

    def hit(self, args):
        if not self.used_dmg:
            self.used_dmg = True
            args.add_damage("GreatWeaponMaster", self.character.prof)
        if args.crit:
            self.bonus_attack_enabled = True

    def after_action(self, target: Target):
        if self.bonus_attack_enabled and self.character.use_bonus("GreatWeaponMaster"):
            self.character.attack(target, self.weapon)


class Archery(Feat):
    def __init__(self) -> None:
        self.name = "Archery"

    def roll_attack(self, args: AttackRollArgs):
        if args.attack.weapon.ranged:
            args.situational_bonus += 2


class DualWielder(Feat):
    def __init__(self):
        self.name = "DualWielder"

    def apply(self, character):
        super().apply(character)
        character.dex += 1


class TwoWeaponFighting(Feat):
    def __init__(self) -> None:
        self.name = "TwoWeaponFighting"

    def roll_attack(self, args: AttackRollArgs):
        if args.attack.has_tag("light"):
            args.attack.remove_tag("light")


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


class Attack(Feat):
    def __init__(self, custom_to_hit=None):
        self.name = "Attack"
        self.custom_to_hit = custom_to_hit

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
        if self.custom_to_hit:
            to_hit = self.custom_to_hit()
        else:
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
        roll_total = roll + to_hit + result.situational_bonus
        log.output(lambda: f"{args.weapon.name} total {roll_total} vs {args.target.ac}")
        if roll_total >= args.target.ac:
            self.character.hit(attack=args, crit=crit, roll=roll)
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
        self.used_savage_attacker = False

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
        if self.savage_attacker and not self.used_savage_attacker:
            self.used_savage_attacker = True
            dmg2 = self.damage(crit=args.crit)
            dmg = max(dmg, dmg2)
        total_dmg = dmg + weapon.bonus
        if args.attack.weapon.base is not None:
            total_dmg += args.attack.weapon.base
        elif not args.attack.has_tag("light"):
            total_dmg += args.attack.character.mod(weapon.mod)
        args.add_damage(f"Weapon:{weapon.name}", total_dmg)
        if weapon.topple:
            if not target.save(args.attack.character.dc(weapon.mod)):
                log.output(lambda: "Knocked prone")
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

    def lowest_slot(self):
        return lowest_spell_slot(self.slots)

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

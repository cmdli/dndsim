from events import AttackRollArgs, HitArgs
from target import Target
from util import (
    get_magic_weapon,
    roll_dice,
)
from character import Character
from feats import ASI, AttackAction, EquipWeapon, GreatWeaponMaster, Feat, Spellcasting
from weapons import Greatsword
from log import log
from spells import DivineSmite


class DivineSmiteFeat(Feat):
    def __init__(self) -> None:
        self.name = "DivineSmite"

    def begin_turn(self, target: Target):
        self.used = False

    def hit(self, args: HitArgs):
        spellcasting = self.character.feat("Spellcasting")
        slot = spellcasting.highest_slot()
        if not self.used and slot >= 1 and self.character.use_bonus("DivineSmite"):
            self.used = True
            spellcasting.cast(DivineSmite(slot))
            num = 1 + slot
            if args.crit:
                num *= 2
            args.add_damage("DivineSmite", roll_dice(num, 8, max_reroll=2))


class ImprovedDivineSmite(Feat):
    def __init__(self) -> None:
        self.name = "ImprovedDivineSmite"

    def hit(self, args: HitArgs):
        num = 2 if args.crit else 1
        args.add_damage("ImprovedDivineSmite", roll_dice(num, 8, max_reroll=2))


class SacredWeapon(Feat):
    def __init__(self) -> None:
        self.name = "SacredWeapon"

    def short_rest(self):
        self.enabled = False

    def begin_turn(self, target: Target):
        if not self.enabled and self.character.use_bonus("SacredWeapon"):
            self.enabled = True

    def roll_attack(self, args: AttackRollArgs):
        if self.enabled:
            args.situational_bonus += self.character.mod("cha")


class Paladin(Character):
    def __init__(self, level):
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        weapon = Greatsword(bonus=magic_weapon)
        base_feats.append(EquipWeapon(weapon=weapon, max_reroll=2))
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(AttackAction(attacks))
        base_feats.append(Spellcasting(level, half=True))
        if level >= 2:
            base_feats.append(DivineSmiteFeat())
        if level >= 11:
            base_feats.append(ImprovedDivineSmite())
        if level >= 3:
            base_feats.append(SacredWeapon())
        feats = [
            GreatWeaponMaster(weapon),
            ASI([["str", 2]]),
            ASI([["cha", 2]]),
            ASI([["cha", 2]]),
            ASI(),
        ]
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 16],
            feats=feats,
            base_feats=base_feats,
        )

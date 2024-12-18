from typing import List

from util.util import get_magic_weapon
from feats import (
    ASI,
    GreatWeaponMaster,
    PolearmMaster,
    AttackAction,
    IrresistibleOffense,
    SavageAttacker,
    WeaponMasteries,
)
from weapons import Glaive, Greatsword, GlaiveButt

import sim.feat
import sim.character
import sim.weapons


class Beserker(sim.feat.Feat):
    def __init__(self, num_dice: int):
        self.used = False
        self.num_dice = num_dice

    def begin_turn(self, target):
        self.used = False

    def attack_result(self, args):
        if args.hits() and not self.used:
            self.used = True
            args.add_damage(source="Berserker", dice=self.num_dice * [6])


class BrutalStrike(sim.feat.Feat):
    def __init__(self, num_dice: int):
        self.num_dice = num_dice

    def begin_turn(self, target):
        self.used = False

    def attack_roll(self, args):
        if not self.used and args.adv:
            args.adv = False
            args.attack.add_tag("brutal_strike")
            self.used = True

    def attack_result(self, args):
        if args.hits() and args.attack.has_tag("brutal_strike"):
            args.add_damage(source="BrutalStrike", dice=self.num_dice * [10])


class Retaliation(sim.feat.Feat):
    def __init__(self, weapon):
        self.weapon = weapon

    def enemy_turn(self, target):
        self.character.weapon_attack(target, weapon=self.weapon)


class PrimalChampion(sim.feat.Feat):
    def apply(self, character):
        super().apply(character)
        character.increase_stat_max("str", 4)
        character.increase_stat_max("con", 4)
        character.increase_stat("str", 4)
        character.increase_stat("con", 4)


class Rage(sim.feat.Feat):
    def __init__(self, dmg):
        self.raging = False
        self.dmg = dmg

    def short_rest(self):
        self.raging = False

    def before_action(self, target):
        if not self.raging and self.character.use_bonus("rage"):
            self.raging = True

    def attack_result(self, args):
        if args.hits() and self.raging:
            args.add_damage(source="Rage", damage=self.dmg)


class RecklessAttack(sim.feat.Feat):
    def begin_turn(self, target):
        self.enabled = True

    def attack_roll(self, args):
        if self.enabled:
            args.adv = True

    def end_turn(self, target):
        self.enabled = False


def rage_damage(level: int):
    if level >= 16:
        return 4
    elif level >= 9:
        return 3
    return 2


class Barbarian(sim.character.Character):
    def __init__(self, level: int, use_pam: bool = False, **kwargs):
        rage_dmg = rage_damage(level)
        magic_weapon = get_magic_weapon(level)
        base_feats: List["sim.feat.Feat"] = []
        base_feats.append(WeaponMasteries(["Graze"]))
        base_feats.append(SavageAttacker())
        base_feats.append(Rage(dmg=rage_dmg))
        base_feats.append(RecklessAttack())
        if use_pam:
            weapon: "sim.weapons.Weapon" = Glaive(magic_bonus=magic_weapon)
        else:
            weapon = Greatsword(magic_bonus=magic_weapon)
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(AttackAction(attacks=attacks))
        if level >= 3:
            base_feats.append(Beserker(num_dice=rage_dmg))
        if level >= 4:
            base_feats.append(GreatWeaponMaster(weapon))
        if level >= 8:
            if use_pam:
                base_feats.append(PolearmMaster(GlaiveButt(magic_bonus=magic_weapon)))
            else:
                base_feats.append(ASI(["str"]))
        if level >= 9:
            base_feats.append(BrutalStrike(num_dice=2 if level >= 17 else 1))
        if level >= 10:
            base_feats.append(Retaliation(weapon))
        if level >= 12 and use_pam:
            base_feats.append(ASI(["dex", "str"]))
        if level >= 19:
            base_feats.append(IrresistibleOffense("str"))
        if level >= 20:
            base_feats.append(PrimalChampion())
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 10],
            base_feats=base_feats,
        )

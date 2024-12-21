from typing import List

from util.util import get_magic_weapon, apply_feats_at_levels
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


class Frenzy(sim.feat.Feat):
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


def barbarian_feats(level: int) -> List["sim.feat.Feat"]:
    rage_dmg = rage_damage(level)
    feats: List["sim.feat.Feat"] = []
    feats.append(WeaponMasteries(["Graze", "Topple"]))
    feats.append(Rage(dmg=rage_dmg))
    # Level 1 (Unarmored Defense) is irrelevant
    if level >= 2:
        feats.append(RecklessAttack())
    # Level 3 (Primal Knowledge) is irrelevant
    # Level 5 (Fast Movement) is irrelevant
    # Level 7 is irrelevant
    if level >= 9:
        feats.append(BrutalStrike(num_dice=2 if level >= 17 else 1))
    # Level 11 is irrelevant
    # Level 15 is irrelevant
    # Level 18 is irrelevant (until Strength checks or saves matter)
    if level >= 20:
        feats.append(PrimalChampion())
    # TODO: Apply ASI feats
    return feats


def berserker_feats(level: int, weapon: "sim.weapons.Weapon") -> List["sim.feat.Feat"]:
    rage_dmg = rage_damage(level)
    feats: List["sim.feat.Feat"] = []
    if level >= 3:
        feats.append(Frenzy(num_dice=rage_dmg))
    # Level 6 is irrelevant
    if level >= 10:
        feats.append(Retaliation(weapon))
    # Level 14 is irrelevant
    return feats


class PolearmBarbarian(sim.character.Character):
    def __init__(self, level: int):
        magic_weapon = get_magic_weapon(level)
        feats: List["sim.feat.Feat"] = []
        weapon = Glaive(magic_bonus=magic_weapon)
        feats.append(AttackAction(attacks=[weapon, weapon] if level >= 5 else [weapon]))
        feats.extend(barbarian_feats(level))
        feats.extend(berserker_feats(level, weapon))
        feats.append(SavageAttacker())
        if level >= 4:
            feats.append(GreatWeaponMaster(weapon))
        if level >= 8:
            feats.append(PolearmMaster(GlaiveButt(magic_bonus=magic_weapon)))
        if level >= 12:
            feats.append(ASI(["dex", "str"]))
        if level >= 16:
            feats.append(ASI(["dex"]))
        if level >= 19:
            feats.append(IrresistibleOffense("str"))
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 10],
            base_feats=feats,
        )


class BerserkerBarbarian(sim.character.Character):
    def __init__(self, level: int, **kwargs):
        magic_weapon = get_magic_weapon(level)
        feats: List["sim.feat.Feat"] = []
        weapon = Greatsword(magic_bonus=magic_weapon)
        feats.append(AttackAction(attacks=[weapon, weapon] if level >= 5 else [weapon]))
        feats.extend(barbarian_feats(level))
        feats.extend(berserker_feats(level, weapon))
        feats.append(SavageAttacker())
        if level >= 4:
            feats.append(GreatWeaponMaster(weapon))
        if level >= 8:
            feats.append(ASI(["str"]))
        if level >= 12:
            feats.append(ASI(["dex"]))
        if level >= 16:
            feats.append(ASI(["dex"]))
        if level >= 19:
            feats.append(IrresistibleOffense("str"))
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 10],
            base_feats=feats,
        )

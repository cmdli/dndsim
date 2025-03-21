#
# My (roughly optimized) 5e character in the old system, Assault Unit 21
# Samarai Fighter, uses the crossbow expert + sharpshooter build
#
import random

from feats import ASI, AttackAction
from util.util import get_magic_weapon
from classes.fighter import ActionSurge
from typing import List

import sim.feat
import sim.character
import sim.target
import sim.weapons


class OldCrossbowExpert(sim.feat.Feat):
    def __init__(self, weapon: sim.weapons.Weapon) -> None:
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.increase_stat("dex", 1)

    def end_turn(self, target):
        if self.character.use_bonus("CrossbowExpert"):
            self.character.weapon_attack(target, self.weapon)


class OldSharpshooter(sim.feat.Feat):
    def apply(self, character):
        super().apply(character)
        character.increase_stat("dex", 1)

    def attack_roll(self, args):
        args.situational_bonus -= 5
        args.attack.add_tag("Sharpshooter")

    def attack_result(self, args):
        if args.hits() and args.attack.has_tag("Sharpshooter"):
            args.add_damage(source="Sharpshooter", damage=10)


class FightingSpirit(sim.feat.Feat):
    def __init__(self, regain_on_initiative: bool = False) -> None:
        self.enabled = False
        self.fighting_spirit = 3
        self.regain_on_initiative = regain_on_initiative

    def long_rest(self):
        self.fighting_spirit = 3

    def short_rest(self):
        if self.regain_on_initiative and self.fighting_spirit == 0:
            self.fighting_spirit = 1

    def before_action(self, target: "sim.target.Target"):
        if self.fighting_spirit > 0 and self.character.use_bonus("FightingSpirit"):
            self.fighting_spirit -= 1
            self.enabled = True

    def attack_roll(self, args):
        if self.enabled:
            args.adv = True

    def end_turn(self, target):
        self.enabled = False


class RapidStrike(sim.feat.Feat):
    def __init__(self) -> None:
        self.used = False

    def begin_turn(self, target: "sim.target.Target"):
        self.used = False

    def attack_roll(self, args):
        weapon = args.attack.weapon
        if weapon and not self.used and args.adv and args.attack.has_tag("main_action"):
            self.used = True
            self.character.weapon_attack(args.attack.target, weapon)


class OldHandCrossbow(sim.weapons.Weapon):
    def __init__(self, **kwargs):
        super().__init__(name="OldHandCrossbow", num_dice=1, die=6, **kwargs)


class Blessed(sim.feat.Feat):
    def attack_roll(self, args):
        args.situational_bonus += random.randint(1, 4)


class AssaultUnit(sim.character.Character):
    def __init__(self, level: int, blessed: bool = False, **kwargs) -> None:
        magic_weapon = get_magic_weapon(level)
        weapon = OldHandCrossbow(bonus=magic_weapon)
        base_feats: List["sim.feat.Feat"] = []
        if level >= 20:
            attacks = 4 * [weapon]
        elif level >= 11:
            attacks = 3 * [weapon]
        elif level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(AttackAction(attacks=attacks))
        if level >= 2:
            base_feats.append(ActionSurge(max_surges=2 if level >= 17 else 1))
        if level >= 3:
            base_feats.append(FightingSpirit(regain_on_initiative=level >= 10))
        if level >= 4:
            base_feats.append(OldCrossbowExpert(weapon))
        if level >= 6:
            base_feats.append(OldSharpshooter())
        if level >= 8:
            base_feats.append(ASI(["dex", "str"]))
        if level >= 15:
            base_feats.append(RapidStrike())
        if blessed:
            base_feats.append(Blessed())
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 10, 10],
            base_feats=base_feats,
        )

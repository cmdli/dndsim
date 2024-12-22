from typing import List, Optional

from util.util import get_magic_weapon, apply_asi_feats
from feats import (
    ASI,
    AttackAction,
    IrresistibleOffense,
    WeaponMaster,
    TavernBrawler,
    Grappler,
)

import sim.core_feats
import sim.feat
import sim.character
import sim.target
import sim.weapons


def martial_arts_die(level: int):
    if level >= 17:
        return 12
    elif level >= 11:
        return 10
    elif level >= 5:
        return 8
    else:
        return 6


class MonkLevel(sim.core_feats.ClassLevels):
    def __init__(self, level: int):
        super().__init__(name="Monk", level=level)


class BodyAndMind(sim.feat.Feat):
    def apply(self, character):
        super().apply(character)
        character.increase_stat_max("dex", 4)
        character.increase_stat_max("wis", 4)
        character.increase_stat("dex", 4)
        character.increase_stat("wis", 4)


class FlurryOfBlows(sim.feat.Feat):
    def __init__(self, num_attacks, weapon):
        self.num_attacks = num_attacks
        self.weapon = weapon

    def before_action(self, target: "sim.target.Target"):
        if self.character.ki.has() and self.character.use_bonus("FlurryOfBlows"):
            self.character.ki.use()
            for _ in range(self.num_attacks):
                self.character.weapon_attack(target, self.weapon, tags=["flurry"])
        elif self.character.use_bonus("BonusAttack"):
            self.character.weapon_attack(target, self.weapon)


class OpenHandTechnique(sim.feat.Feat):
    def attack_result(self, args):
        if args.hits() and args.attack.has_tag("flurry"):
            if not args.attack.target.save(self.character.dc("wis")):
                args.attack.target.knock_prone()


class StunningStrike(sim.feat.Feat):
    def __init__(self, level: int, avoid_on_grapple: bool = False):
        self.weapon_die = martial_arts_die(level)
        self.stuns: List[int] = []
        self.avoid_on_grapple = avoid_on_grapple

    def begin_turn(self, target: "sim.target.Target"):
        self.used = False
        target.stunned = False

    def attack_result(self, args):
        target = args.attack.target
        if args.misses() or self.used or not self.character.ki.has():
            return
        if target.grappled and self.avoid_on_grapple:
            return
        if target.stunned:
            return
        self.used = True
        self.character.ki.use()
        if not target.save(self.character.dc("wis")):
            target.stunned = True
        else:
            target.semistunned = True


class Ki(sim.feat.Feat):
    def __init__(self, max_ki):
        self.max_ki = max_ki

    def apply(self, character):
        super().apply(character)
        character.ki.increase_max(self.max_ki)


class Fists(sim.weapons.Weapon):
    def __init__(self, weapon_die, **kwargs):
        super().__init__(
            name="Fists",
            num_dice=1,
            die=weapon_die,
            tags=["finesse"],
            **kwargs,
        )


def monk_feats(
    level: int, asis: Optional[List["sim.feat.Feat"]]
) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 1:
        feats.append(MonkLevel(level))
    # Level 1 (Unarmored Defense) is irrelevant
    if level >= 2:
        feats.append(Ki(level))
    # TODO: Level 2 (Uncanny Metabolism)
    # Level 3 (Deflect Attacks) is irrelevant/ignored
    # Level 4 (Slow Fall) is irrelevant
    if level >= 5:
        feats.append(StunningStrike(level, avoid_on_grapple=True))
    # Level 6 (Empowered Strikes) is irrelevant
    # Level 7 (Evasion) is irrelevant
    # Level 9 (Acrobatic Movement) is irrelevant
    # Level 10 (Self-Restoration) is irrelevant
    # Level 13 (Deflect Energy) is irrelevant
    # Level 14 (Disciplined Survivor) is irrelevant
    # TODO: Level 15 (Perfect Focus)
    # Level 18 (Superior Defense) is irrelevant
    if level >= 20:
        feats.append(BodyAndMind())
    apply_asi_feats(level=level, feats=feats, asis=asis)
    return feats


def open_hand_monk_feats(level: int) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 3:
        feats.append(OpenHandTechnique())
    # Level 6 (Wholeness of Body) is irrelevant
    # Level 11 (Fleet Step) is irrelevant
    # TODO: Level 17 (Quivering Palm)
    return feats


class DefaultMonkAction(sim.feat.Feat):
    def __init__(self, level: int, weapon: "sim.weapons.Weapon"):
        self.level = level
        self.weapon = weapon

    def action(self, target):
        num_attacks = 1
        if self.character.has_class_level("Monk", 5):
            num_attacks = 2
        for i in range(num_attacks):
            self.character.weapon_attack(target, self.weapon, tags=["main_action"])
        if (
            self.character.has_class_level("Monk", 2)
            and self.character.ki.has()
            and self.character.use_bonus("FlurryOfBlows")
        ):
            self.character.ki.use()
            num_attacks = 2
            if self.character.has_class_level("Monk", 10):
                num_attacks = 3
            for _ in range(num_attacks):
                self.character.weapon_attack(target, self.weapon, tags=["flurry"])
        if self.character.use_bonus("BonusAttack"):
            self.character.weapon_attack(target, self.weapon)


class OpenHandMonk(sim.character.Character):
    def __init__(self, level: int, **kwargs):
        magic_weapon = get_magic_weapon(level)
        feats: List[sim.feat.Feat] = []
        weapon_die = martial_arts_die(level)
        fists = Fists(weapon_die, magic_bonus=magic_weapon)
        feats.append(TavernBrawler())
        feats.extend(
            monk_feats(
                level=level,
                asis=[
                    Grappler("dex"),
                    ASI(["dex"]),
                    ASI(["wis"]),
                    ASI(["wis"]),
                    IrresistibleOffense("dex"),
                ],
            )
        )
        feats.extend(open_hand_monk_feats(level))
        feats.append(DefaultMonkAction(level, fists))
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            base_feats=feats,
        )

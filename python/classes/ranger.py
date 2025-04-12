from typing import List, override, Optional

import sim.core_feats
from sim.events import DamageRollArgs
from util.util import get_magic_weapon, apply_asi_feats
from feats.epic_boons import IrresistibleOffense
from feats.fighting_style import TwoWeaponFighting, Archery
from feats import (
    ASI,
    CrossbowExpert,
    DualWielder,
    WeaponMasteries,
    LightWeaponBonusAttack,
)
from weapons import HandCrossbow, Shortsword, Scimitar, Rapier
from spells.ranger import HuntersMark
from spells.summons import SummonFey
from sim.spells import Spellcaster


import sim.feat
import sim.character
import sim.target
import sim.weapons


def maybe_cast_summon_fey(
    character: "sim.character.Character",
    summon_fey_threshold: int,
):
    slot = character.spells.highest_slot()
    if slot >= summon_fey_threshold and not character.spells.is_concentrating():
        spell = SummonFey(slot)
        character.spells.cast(spell)
        return True
    return False


def maybe_cast_hunters_mark(
    character: "sim.character.Character",
    target: "sim.target.Target",
):
    slot = character.spells.lowest_slot()
    if (
        slot > 0
        and not character.spells.is_concentrating()
        and character.use_bonus("HuntersMark")
    ):
        character.spells.cast(HuntersMark(slot), target)
        return True
    return False


class RangerLevel(sim.core_feats.ClassLevels):
    def __init__(self, level: int):
        super().__init__(name="Ranger", level=level, spellcaster=Spellcaster.HALF)


class BestialFury(sim.feat.Feat):
    def __init__(
        self,
        caster: Optional["sim.character.Character"] = None,
    ) -> None:
        self.caster = caster

    def apply(self, character: "sim.character.Character"):
        super().apply(character)
        if self.caster is None:
            self.caster = character

    def attack_result(self, args):
        if args.hits() and args.attack.target.has_tag("HuntersMark"):
            args.add_damage(
                source="HuntersMark",
                dice=[6],
            )


class FoeSlayer(sim.feat.Feat):
    def damage_roll(self, args: DamageRollArgs):
        if args.damage.source == "HuntersMark":
            for i in range(len(args.damage.dice)):
                args.damage.dice[i] = 8
            args.damage.reroll()


class PreciseHunter(sim.feat.Feat):
    def attack_roll(self, args):
        if args.attack.target.has_tag("HuntersMark"):
            args.adv = True


class DreadAmbusher(sim.feat.Feat):
    def __init__(self, level: int) -> None:
        self.die = 8 if level >= 11 else 6
        self.uses = 0

    def long_rest(self):
        self.uses = self.character.mod("wis")

    def begin_turn(self, target: "sim.target.Target"):
        self.used = False

    def attack_result(self, args):
        if args.hits() and not self.used and self.uses > 0:
            self.used = True
            self.uses -= 1
            args.add_damage(source="DreadAmbusher", dice=2 * [self.die])


class BeastChargeFeat(sim.feat.Feat):
    def __init__(self, character: "sim.character.Character"):
        self.character = character

    def attack_result(self, args):
        if args.hits() and isinstance(args.attack.weapon, BeastMaul):
            args.add_damage(source="Charge", dice=[6])
            if not args.attack.target.prone and not args.attack.target.save(
                self.character.dc("wis")
            ):
                args.attack.target.knock_prone()


def ranger_feats(
    level: int,
    masteries: List["sim.weapons.WeaponMastery"],
    fighting_style: "sim.feat.Feat",
    asis: Optional[List["sim.feat.Feat"]] = None,
) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 1:
        feats.append(RangerLevel(level))
        feats.append(WeaponMasteries(masteries))
    # Level 2 (Deft Explorer) is irrelevant
    if level >= 2:
        feats.append(fighting_style)
    # Level 6 (Roving) is irrelevant
    # Level 9 (Expertise) is irrelevant
    # Level 10 (Tireless) is irrelevant
    # Level 13 (Relentless Hunter) is irrelevant
    # TODO: Level 14 (Nature's Veil)
    if level >= 17:
        feats.append(PreciseHunter())
    # Level 18 (Feral Senses) is irrelevant
    if level >= 20:
        feats.append(FoeSlayer())
    apply_asi_feats(level=level, feats=feats, asis=asis)
    return feats


def gloomstalker_ranger_feats(
    level: int, weapon: "sim.weapons.Weapon"
) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 3:
        feats.append(DreadAmbusher(level))
    # Level 3 (Umbral Sight) is irrelevant
    # Level 7 (Iron Mind) is irrelevant
    # Level 11 (Stalker's Flurry) is handled elsewhere
    # Level 15 (Shadowy Dodge) is irrelevant
    return feats


class GloomstalkerAction(sim.feat.Feat):
    def __init__(
        self, attacks: List["sim.weapons.Weapon"], summon_fey_threshold: int
    ) -> None:
        self.attacks = attacks
        self.summon_fey_threshold = summon_fey_threshold

    def action(self, target: "sim.target.Target"):
        if maybe_cast_summon_fey(self.character, self.summon_fey_threshold):
            return
        maybe_cast_hunters_mark(self.character, target)
        for weapon in self.attacks:
            self.character.weapon_attack(target, weapon, tags=["main_action"])
        self.character.weapon_attack(target, self.attacks[0], tags=["light"])


class GloomstalkerRanger(sim.character.Character):
    def __init__(self, level: int):
        magic_weapon = get_magic_weapon(level)
        feats: List["sim.feat.Feat"] = []
        weapon: "sim.weapons.Weapon" = HandCrossbow(magic_bonus=magic_weapon)
        attacks: List["sim.weapons.Weapon"] = [weapon]
        if level >= 5:
            attacks = 2 * [weapon]
        feats.append(GloomstalkerAction(attacks=attacks, summon_fey_threshold=4))
        feats.extend(
            ranger_feats(
                level=level,
                masteries=["Vex", "Nick"],
                fighting_style=Archery(),
                asis=[
                    CrossbowExpert(weapon),
                    ASI(["dex"]),
                    ASI(["wis"]),
                    ASI(["wis"]),
                    IrresistibleOffense("dex"),
                ],
            )
        )
        feats.extend(gloomstalker_ranger_feats(level, weapon))
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            base_feats=feats,
            spell_mod="wis",
        )


class PrimalCompanion(sim.character.Character):
    def __init__(self, level: int, ranger: "sim.character.Character"):
        self.ranger = ranger
        self.num_attacks = 2 if level >= 11 else 1
        self.weapon = BeastMaul(self)
        feats: List["sim.feat.Feat"] = []
        feats.append(BeastChargeFeat(ranger))
        if level >= 11:
            feats.append(BestialFury(caster=ranger))
        if level >= 20:
            feats.append(FoeSlayer())
        super().init(
            level=level,
            stats=[10, 10, 10, 10, 10, 10],
            base_feats=feats,
        )

    def do_attack(self, target: "sim.target.Target"):
        for _ in range(self.num_attacks):
            self.weapon_attack(target, self.weapon)


class BeastMaul(sim.weapons.Weapon):
    def __init__(self, ranger: "sim.character.Character", **kwargs):
        super().__init__(name="Beast Maul", num_dice=1, die=8, **kwargs)
        self.ranger = ranger

    @override
    def to_hit(self, character):
        return self.ranger.spells.to_hit()

    @override
    def attack_result(self, args, character):
        if not args.hits():
            return
        num_dice = 2 if args.crit else 1
        args.add_damage(
            source=self.name,
            dice=num_dice * [8],
            damage=2 + self.ranger.mod("wis"),
        )


class BeastMasterAction(sim.feat.Feat):
    def __init__(
        self,
        level: int,
        beast: PrimalCompanion,
        magic_bonus: int,
    ) -> None:
        self.beast = beast
        self.shortsword = Shortsword(magic_bonus=magic_bonus)
        self.scimitar = Scimitar(magic_bonus=magic_bonus)
        if level >= 4:
            self.main_hand: "sim.weapons.Weapon" = Rapier(magic_bonus=magic_bonus)
        else:
            self.main_hand = Shortsword(magic_bonus=magic_bonus)

    def action(self, target: "sim.target.Target"):
        if maybe_cast_summon_fey(self.character, summon_fey_threshold=4):
            return
        maybe_cast_hunters_mark(self.character, target)
        if self.character.level >= 3:
            commanded_beast = False
            if self.character.use_bonus("beast"):
                self.beast.do_attack(target)
                commanded_beast = True
            num_attacks = 2 if self.character.level >= 5 else 1
            for _ in range(num_attacks):
                if not commanded_beast:
                    self.beast.do_attack(target)
                    commanded_beast = True
                else:
                    self.character.weapon_attack(target, self.main_hand)
            self.character.weapon_attack(target, self.shortsword, tags=["light"])
        else:
            self.character.weapon_attack(target, self.main_hand)
            # Use bonus action to use Vex weapon, if possible
            if self.character.use_bonus("light weapon"):
                self.character.weapon_attack(target, self.scimitar, tags=["light"])
            else:
                self.character.weapon_attack(target, self.shortsword, tags=["light"])


def beast_master_ranger_feats(level: int) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    # TODO: Move Primal Companion into here
    # Level 7 (Exceptional Training) is irrelevant
    # Level 11 (Bestial Fury) is handled elsewhere
    # TODO: Level 15 (Share Spells)
    return feats


class BeastMasterRanger(sim.character.Character):
    def __init__(self, level: int):
        magic_weapon = get_magic_weapon(level)
        feats: List["sim.feat.Feat"] = []
        beast = PrimalCompanion(level, ranger=self)
        shortsword = Shortsword(magic_bonus=magic_weapon)
        feats.append(
            BeastMasterAction(
                level=level,
                beast=beast,
                magic_bonus=magic_weapon,
            )
        )
        feats.extend(
            ranger_feats(
                level=level,
                masteries=["Vex", "Nick"],
                fighting_style=TwoWeaponFighting(),
                asis=[
                    DualWielder("dex", shortsword),
                    ASI(["dex"]),
                    ASI(["wis"]),
                    ASI(["wis"]),
                    IrresistibleOffense("dex"),
                ],
            )
        )
        feats.extend(beast_master_ranger_feats(level))
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            base_feats=feats,
            spell_mod="wis",
        )
        self.add_minion(beast)

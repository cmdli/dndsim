from typing import List, Optional

from feats import (
    ASI,
    DualWielder,
    WarCaster,
    SpellSniper,
    ElvenAccuracy,
    Archery,
)
import sim.core_feats
from weapons import Shortsword, Scimitar, HandCrossbow, Dagger
from util.util import get_magic_weapon, apply_asi_feats
from spells.wizard import TrueStrike
from spells.paladin import HolyWeapon
from spells.warlock import EldritchBlast
from spells.druid import ConjureMinorElementals
from sim.spells import Spellcaster

import sim.weapons
import sim.feat
import sim.character
import sim.target
import classes.fighter
import classes.warlock


def inspiration_die(level: int):
    if level >= 15:
        return 12
    if level >= 10:
        return 10
    if level >= 5:
        return 8
    return 6


class PactHandCrossbow(HandCrossbow):
    def mod(self, character):
        return "cha"


class BardLevel(sim.core_feats.ClassLevels):
    def __init__(self, level: int):
        super().__init__(name="Bard", level=level, spellcaster=Spellcaster.FULL)


class BardicInspiration(sim.feat.Feat):
    def __init__(self, level: int):
        self.level = level

    def apply(self, character):
        super().apply(character)
        character.bardic_inspiration.die = inspiration_die(self.level)

    def long_rest(self):
        self.character.bardic_inspiration.num = self.character.mod("cha")


class FontOfInspiration(sim.feat.Feat):
    def short_rest(self):
        self.character.bardic_inspiration.num = self.character.mod("cha")


class SuperiorInspiration(sim.feat.Feat):
    # TODO: Add this when we don't take short rests between every encounter
    pass


def bard_feats(
    level: int, asis: Optional[List["sim.feat.Feat"]] = None
) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 1:
        feats.append(BardLevel(level))
        feats.append(BardicInspiration(level))
    # Level 2 (Expertise) is irrelevant
    # Level 2 (Jack of all Trades) is irrelevant
    if level >= 5:
        feats.append(FontOfInspiration())
    # Level 7 (Countercharm) is irrelevant
    # Level 10 (Magical Secrets) is expected to be handled by the caller
    if level >= 18:
        feats.append(SuperiorInspiration())
    # TODO: Level 20 (Words of Creation)
    apply_asi_feats(level=level, feats=feats, asis=asis)
    return feats


def valor_feats(level: int) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    # Level 3 (Combat Inspiration) is useless because we cannot inspire ourselves
    # Level 3 (Martial Training) is irrelevant because weapon proficiencies are ignored
    # Level 6 (Extra Attack) is expected to be handled by the action feat
    # TODO: Level 14 (Battle Magic)
    return feats


class TrueStrikeAction(sim.feat.Feat):
    def __init__(
        self,
        truestrike_weapon: "sim.weapons.Weapon",
        attacks: List["sim.weapons.Weapon"],
        nick_attacks: List["sim.weapons.Weapon"],
        use_holy_weapon: bool = False,
    ) -> None:
        self.truestrike_weapon = truestrike_weapon
        self.attacks = attacks
        self.nick_attacks = nick_attacks
        self.use_holy_weapon = use_holy_weapon

    def action(self, target: "sim.target.Target"):
        slot = self.character.spells.highest_slot()
        if (
            self.use_holy_weapon
            and slot >= 5
            and not self.character.has_effect("HolyWeapon")
            and self.character.use_bonus("HolyWeapon")
        ):
            self.character.spells.cast(HolyWeapon(slot, weapon=self.truestrike_weapon))
        self.character.spells.cast(TrueStrike(self.truestrike_weapon), target)
        for attack in self.attacks:
            self.character.weapon_attack(target, attack)
        for attack in self.nick_attacks:
            self.character.weapon_attack(target, attack, tags=["light"])


class ValorBardBonusAttack(sim.feat.Feat):
    def __init__(self, weapon: "sim.weapons.Weapon") -> None:
        self.weapon = weapon

    def after_action(self, target: "sim.target.Target"):
        if self.character.use_bonus("ValorBardBonusAttack"):
            self.character.weapon_attack(target, self.weapon)


class ValorBard(sim.character.Character):
    def __init__(self, level: int, **kwargs) -> None:
        magic_weapon = get_magic_weapon(level)
        feats: List["sim.feat.Feat"] = []
        weapon = Shortsword(magic_bonus=magic_weapon)
        scimitar = Scimitar(magic_bonus=magic_weapon)
        attacks: List["sim.weapons.Weapon"] = []
        if level >= 6:
            attacks = [weapon]
        feats.append(
            TrueStrikeAction(
                weapon,
                attacks=attacks,
                nick_attacks=[scimitar],
                use_holy_weapon=level >= 10,
            )
        )
        feats.extend(
            bard_feats(
                level=level,
                asis=[
                    ASI(["cha"]),
                    ASI(["cha", "dex"]),
                    ASI(["dex"]),
                    ASI(["dex", "wis"]),
                ],
            )
        )
        feats.extend(valor_feats(level))
        if level >= 14:
            # TODO: Handle this in the Valor Bard feats
            feats.append(ValorBardBonusAttack(weapon))
        super().init(
            level=level,
            stats=[10, 16, 10, 10, 10, 17],
            base_feats=feats,
            spell_mod="cha",
        )


class CMEMulticlassAction(sim.feat.Feat):
    def __init__(
        self,
        level: int,
        weapon: "sim.weapons.Weapon",
        nick_weapon: Optional["sim.weapons.Weapon"] = None,
    ) -> None:
        self.level = level
        self.weapon = weapon
        self.nick_weapon = nick_weapon
        self.used_nick = False

    def begin_turn(self, target: "sim.target.Target"):
        self.used_nick = False

    def action(self, target):
        if (
            self.character.has_class_level("Bard", 10)
            and not self.character.spells.is_concentrating()
        ):
            slot = self.character.spells.highest_slot()
            if slot >= 4:
                self.character.spells.cast(ConjureMinorElementals(slot))
                return
        if self.character.has_class_level("Bard", 6):
            # Two attacks
            if self.character.has_class_level("Warlock", 1):
                self.character.spells.cast(EldritchBlast(self.level), target)
                self.character.weapon_attack(target, self.weapon)
            else:
                self.character.spells.cast(TrueStrike(self.weapon), target)
                self.character.weapon_attack(target, self.weapon)
        else:
            # One attack
            if self.character.has_class_level("Warlock", 1):
                self.character.spells.cast(EldritchBlast(self.level), target)
            else:
                self.character.spells.cast(TrueStrike(self.weapon), target)
        if not self.used_nick and self.nick_weapon is not None:
            self.used_nick = True
            self.character.weapon_attack(target, self.nick_weapon)
        if self.character.has_class_level("Bard", 14):
            self.character.weapon_attack(target, self.weapon)


class CMEMulticlass(sim.character.Character):
    def __init__(self, level: int) -> None:
        magic_weapon = get_magic_weapon(level)
        feats: List["sim.feat.Feat"] = []
        class_levels = {
            "fighter": 0,
            "warlock": 0,
            "bard": 0,
        }
        levelups = [
            "fighter",
            "bard",
            "bard",
            "bard",
            "bard",
            "bard",
            "bard",
            "warlock",
            "bard",
            "bard",
            "bard",
            "bard",
            "fighter",
            "bard",
            "bard",
            "bard",
            "bard",
            "bard",
            "bard",
            "bard",
        ]
        for i in range(level):
            class_levels[levelups[i]] += 1
        feats.extend(
            classes.fighter.fighter_feats(
                class_levels["fighter"],
                masteries=["Nick", "Vex"],
                fighting_style=Archery(),
            )
        )
        feats.extend(
            bard_feats(
                class_levels["bard"],
                asis=[
                    WarCaster("cha"),
                    SpellSniper("cha"),
                    ElvenAccuracy("cha"),
                    ASI(["dex"]),
                ],
            )
        )
        feats.extend(classes.warlock.warlock_feats(class_levels["warlock"]))
        feats.append(classes.warlock.AgonizingBlast())

        crossbow = (
            PactHandCrossbow(magic_bonus=magic_weapon)
            if class_levels["warlock"] > 0
            else HandCrossbow(magic_bonus=magic_weapon)
        )
        scimitar = Scimitar(magic_bonus=magic_weapon)
        feats.append(
            CMEMulticlassAction(level=level, weapon=crossbow, nick_weapon=scimitar)
        )
        super().init(
            level=level,
            stats=[10, 16, 10, 10, 10, 17],
            base_feats=feats,
            spell_mod="cha",
        )

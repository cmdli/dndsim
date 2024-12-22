from typing import List, Optional

import sim.core_feats
from util.util import get_magic_weapon, apply_asi_feats
from feats import (
    ASI,
    AttackAction,
    GreatWeaponMaster,
    TwoWeaponFighting,
    GreatWeaponFighting,
    WeaponMasteries,
    IrresistibleOffense,
    ChannelDivinity,
)
from weapons import Greatsword, Shortsword, Scimitar
from spells.paladin import DivineFavor, DivineSmite
from sim.spells import Spellcaster

import sim.weapons
import sim.feat
import sim.character
import sim.target


class PaladinLevel(sim.core_feats.ClassLevels):
    def __init__(self, level: int):
        super().__init__(name="Paladin", level=level, spellcaster=Spellcaster.HALF)


class DivineSmiteFeat(sim.feat.Feat):
    def attack_result(self, args):
        if args.misses():
            return
        slot = self.character.spells.highest_slot()
        if slot >= 1 and self.character.use_bonus("DivineSmite"):
            self.character.spells.cast(
                DivineSmite(slot=slot, crit=args.crit), target=args.attack.target
            )


class RadiantStrikes(sim.feat.Feat):
    def attack_result(self, args):
        if args.hits():
            args.add_damage(source="RadiantStrikes", dice=[8])


class SacredWeapon(sim.feat.Feat):
    def short_rest(self):
        self.enabled = False

    def begin_turn(self, target: "sim.target.Target"):
        if not self.enabled and self.character.channel_divinity.use():
            self.enabled = True

    def attack_roll(self, args):
        if self.enabled:
            args.situational_bonus += self.character.mod("cha")


class DivineFavorFeat(sim.feat.Feat):
    def begin_turn(self, target: "sim.target.Target"):
        slot = self.character.spells.lowest_slot()
        if (
            not self.character.spells.is_concentrating()
            and slot >= 1
            and self.character.use_bonus("DivineFavor")
        ):
            self.character.spells.cast(DivineFavor(slot))


def paladin_feats(
    level: int,
    masteries: List["sim.weapons.WeaponMastery"],
    fighting_style: "sim.feat.Feat",
    asis: Optional[List["sim.feat.Feat"]] = None,
) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 1:
        feats.append(PaladinLevel(level))
        feats.append(WeaponMasteries(masteries))
    if level >= 2:
        feats.append(fighting_style)
        feats.append(DivineSmiteFeat())
    if level >= 3:
        feats.append(ChannelDivinity(uses=2))
    # TODO: Level 5 (Faithful Steed)
    # Level 6 (Aura of Protection) is irrelevant
    # Level 9 (Abjure Foes) is irrelevant
    # Level 10 (Aura of Courage) is irrelevant
    if level >= 11:
        feats.append(RadiantStrikes())
        feats.append(ChannelDivinity(uses=1))
    # Level 14 (Reestoring Touch) is irrelevant
    # Level 18 (Aura Expansion) is irrelevant
    apply_asi_feats(level=level, feats=feats, asis=asis)
    return feats


def devotion_paladin_feats(level: int) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 3:
        feats.append(SacredWeapon())
    # Level 7 (Aura of Devotion) is irrelevant
    # Level 15 (Smite of Protection) is irrelevant
    # TODO: Level 20 (Holy Nimbus)
    return feats


class DevotionPaladin(sim.character.Character):
    def __init__(self, level: int, use_twf=False, **kwargs):
        magic_weapon = get_magic_weapon(level)
        feats: List["sim.feat.Feat"] = []
        feats.append(DivineFavorFeat())
        if use_twf:
            masteries = ["Vex", "Nick"]
            fighting_style = TwoWeaponFighting()
            weapon: "sim.weapons.Weapon" = Shortsword(magic_bonus=magic_weapon)
            nick_attacks = [Scimitar(magic_bonus=magic_weapon)]
        else:
            masteries = ["Graze", "Topple"]
            fighting_style = GreatWeaponFighting()
            weapon = Greatsword(magic_bonus=magic_weapon)
            nick_attacks = []
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        feats.append(AttackAction(attacks=attacks, nick_attacks=nick_attacks))
        first_feat = ASI(["str", "con"]) if use_twf else GreatWeaponMaster(weapon)
        feats.extend(
            paladin_feats(
                level,
                masteries=masteries,
                fighting_style=fighting_style,
                asis=[
                    first_feat,
                    ASI(["str"]),
                    ASI(["cha"]),
                    ASI(["cha"]),
                    IrresistibleOffense("str"),
                ],
            )
        )
        feats.extend(devotion_paladin_feats(level))
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 16],
            base_feats=feats,
            spell_mod="cha",
        )

from typing import List

from util.util import get_magic_weapon
from feats import (
    ASI,
    AttackAction,
    GreatWeaponMaster,
    TwoWeaponFighting,
    GreatWeaponFighting,
    WeaponMasteries,
    IrresistibleOffense,
)
from weapons import Greatsword, Shortsword, Scimitar
from spells.paladin import DivineFavor, DivineSmite
from sim.spells import Spellcaster

import sim.weapons
import sim.feat
import sim.character
import sim.target


class DivineSmiteFeat(sim.feat.Feat):
    def begin_turn(self, target: "sim.target.Target"):
        self.used = False

    def attack_result(self, args):
        if args.misses():
            return
        slot = self.character.spells.highest_slot()
        if not self.used and slot >= 1 and self.character.use_bonus("DivineSmite"):
            self.used = True
            self.character.spells.cast(
                DivineSmite(slot, args.crit), target=args.attack.target
            )


class ImprovedDivineSmite(sim.feat.Feat):
    def attack_result(self, args):
        if args.hits():
            args.add_damage(source="ImprovedDivineSmite", dice=[8])


class SacredWeapon(sim.feat.Feat):
    def short_rest(self):
        self.enabled = False

    def begin_turn(self, target: "sim.target.Target"):
        if not self.enabled and self.character.use_bonus("SacredWeapon"):
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


class Paladin(sim.character.Character):
    def __init__(self, level: int, use_twf=False, **kwargs):
        magic_weapon = get_magic_weapon(level)
        base_feats: List["sim.feat.Feat"] = []
        base_feats.append(DivineFavorFeat())
        if use_twf:
            base_feats.append(WeaponMasteries(["Vex", "Nick"]))
            base_feats.append(TwoWeaponFighting())
            weapon: "sim.weapons.Weapon" = Shortsword(magic_bonus=magic_weapon)
            nick_attacks = [Scimitar(magic_bonus=magic_weapon)]
        else:
            base_feats.append(WeaponMasteries(["Graze", "Topple"]))
            base_feats.append(GreatWeaponFighting())
            weapon = Greatsword(magic_bonus=magic_weapon)
            nick_attacks = []
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(AttackAction(attacks=attacks, nick_attacks=nick_attacks))
        if level >= 2:
            base_feats.append(DivineSmiteFeat())
        if level >= 3:
            base_feats.append(SacredWeapon())
        if level >= 4:
            if use_twf:
                base_feats.append(ASI(["str", "con"]))
            else:
                base_feats.append(GreatWeaponMaster(weapon))
        if level >= 8:
            base_feats.append(ASI(["str"]))
        if level >= 11:
            base_feats.append(ImprovedDivineSmite())
        if level >= 12:
            base_feats.append(ASI(["cha"]))
        if level >= 16:
            base_feats.append(ASI(["cha"]))
        if level >= 19:
            base_feats.append(IrresistibleOffense("str"))
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 16],
            base_feats=base_feats,
            spellcaster=Spellcaster.HALF,
        )

from typing import List

from feats import ASI, DualWielder
from weapons import Shortsword, Scimitar
from util.util import get_magic_weapon
from spells.wizard import TrueStrike
from spells.paladin import HolyWeapon
from spells.warlock import EldritchBlast
from sim.spells import Spellcaster

import sim.weapons
import sim.feat
import sim.character
import sim.target


# TODO: Refactor this into a spell
class TrueStrikeFeat(sim.feat.Feat):
    def __init__(self, level: int, spell_mod: str) -> None:
        self.spell_mod = spell_mod
        if level >= 17:
            self.num_dice = 3
        elif level >= 11:
            self.num_dice = 2
        elif level >= 5:
            self.num_dice = 1
        else:
            self.num_dice = 0

    def attack_roll(self, args):
        weapon = args.attack.weapon
        if weapon and args.attack.has_tag("truestrike"):
            args.situational_bonus += self.character.mod(
                self.spell_mod
            ) - self.character.mod(weapon.mod(self.character))

    def attack_result(self, args):
        if args.hits() and args.attack.has_tag("truestrike"):
            args.add_damage(source="TrueStrike", dice=self.num_dice * [6])


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
        base_feats: List["sim.feat.Feat"] = []
        weapon = Shortsword(magic_bonus=magic_weapon)
        scimitar = Scimitar(magic_bonus=magic_weapon)
        base_feats.append(TrueStrikeFeat(level, "cha"))
        attacks: List["sim.weapons.Weapon"] = []
        if level >= 6:
            attacks = [weapon]
        base_feats.append(
            TrueStrikeAction(
                weapon,
                attacks=attacks,
                nick_attacks=[scimitar],
                use_holy_weapon=level >= 10,
            )
        )
        if level >= 4:
            base_feats.append(ASI(["cha"]))
        if level >= 8:
            base_feats.append(ASI(["cha", "dex"]))
        if level >= 12:
            base_feats.append(ASI(["dex"]))
        if level >= 14:
            base_feats.append(ValorBardBonusAttack(weapon))
        if level >= 16:
            base_feats.append(ASI(["dex", "wis"]))
        super().init(
            level=level,
            stats=[10, 16, 10, 10, 10, 17],
            base_feats=base_feats,
            spellcaster=Spellcaster.FULL,
            spell_mod="cha",
        )


class CMEMulticlassAction(sim.feat.Feat):
    def __init__(self, level: int, weapon: "sim.weapons.Weapon") -> None:
        self.level = level
        self.weapon = weapon

    def action(self, target):
        if self.level >= 7:
            self.character.spells.cast(EldritchBlast(self.level))
        self.character.weapon_attack(target, self.weapon)
        self.character.weapon_attack(target, self.weapon)


class CMEMulticlass(sim.character.Character):
    def __init__(self, level: int) -> None:
        # Valor Bard 5
        # Warlock 1
        # Valor Bard 19
        base_feats: List[sim.feat.Feat] = []
        weapon = Scimitar()
        base_feats.append(CMEMulticlassAction(level, weapon))
        if level >= 4:
            base_feats.append(DualWielder("dex", weapon))
        if level >= 8:
            base_feats.append(ASI(["dex"]))
        if level >= 12:
            base_feats.append(ASI(["cha"]))
        if level >= 16:
            base_feats.append(ASI(["cha", "wis"]))
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 10, 16],
            base_feats=base_feats,
            spellcaster=Spellcaster.FULL,
            spell_mod="cha",
        )

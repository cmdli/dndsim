from sim.character import Character
from sim.feats import Feat, ASI, AttackAction, DualWielder
from sim.weapons import Weapon, Shortsword, Scimitar
from sim.events import AttackRollArgs
from util.util import roll_dice, get_magic_weapon
from sim.target import Target
from typing import List
from spells.wizard import TrueStrike
from spells.paladin import HolyWeapon
from spells.warlock import EldritchBlast
from sim.spellcasting import Spellcaster


# TODO: Refactor this into a spell
class TrueStrikeFeat(Feat):
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

    def attack_roll(self, args: AttackRollArgs):
        weapon = args.attack.weapon
        if weapon and args.attack.has_tag("truestrike"):
            args.situational_bonus += self.character.mod(
                self.spell_mod
            ) - self.character.mod(weapon.mod(self.character))

    def attack_result(self, args):
        if args.hits() and args.attack.has_tag("truestrike"):
            args.add_damage_dice("TrueStrike", self.num_dice, 6)


class TrueStrikeAction(Feat):
    def __init__(
        self,
        truestrike_weapon: Weapon,
        attacks: List[Weapon],
        nick_attacks: List[Weapon],
    ) -> None:
        self.truestrike_weapon = truestrike_weapon
        self.attacks = attacks
        self.nick_attacks = nick_attacks

    def action(self, target: Target):
        self.character.spells.cast(TrueStrike(self.truestrike_weapon), target)
        for attack in self.attacks:
            self.character.weapon_attack(target, attack)
        for attack in self.nick_attacks:
            self.character.weapon_attack(target, attack, tags=["light"])


class HolyWeaponFeat(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.weapon = weapon

    def before_action(self, target: Target):
        if not self.character.has_effect("HolyWeapon") and self.character.use_bonus(
            "HolyWeapon"
        ):
            self.character.spells.cast(HolyWeapon(self.character.spells.highest_slot()))

    def attack_result(self, args):
        if args.hits() and args.attack.weapon.name == self.weapon.name:
            args.add_damage_dice("HolyWeapon", 2, 8)


class ValorBardBonusAttack(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.weapon = weapon

    def after_action(self, target: Target):
        if self.character.use_bonus("ValorBardBonusAttack"):
            self.character.weapon_attack(target, self.weapon)


class ValorBard(Character):
    def __init__(self, level: int, **kwargs) -> None:
        magic_weapon = get_magic_weapon(level)
        base_feats: List[Feat] = []
        weapon = Shortsword(magic_bonus=magic_weapon)
        scimitar = Scimitar(magic_bonus=magic_weapon)
        base_feats.append(TrueStrikeFeat(level, "cha"))
        attacks: List[Weapon] = []
        if level >= 6:
            attacks = [weapon]
        base_feats.append(
            TrueStrikeAction(weapon, attacks=attacks, nick_attacks=[scimitar])
        )
        if level >= 4:
            base_feats.append(ASI(["cha"]))
        if level >= 8:
            base_feats.append(ASI(["cha", "dex"]))
        if level >= 10:
            base_feats.append(HolyWeaponFeat(weapon))
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


class CMEMulticlassAction(Feat):
    def __init__(self, level: int, weapon: Weapon) -> None:
        self.level = level
        self.weapon = weapon

    def action(self, target):
        if self.level >= 7:
            self.character.cast(EldritchBlast(self.level))
        self.character.weapon_attack(target, self.weapon)
        self.character.weapon_attack(target, self.weapon)


class CMEMulticlass(Character):
    def __init__(self, level: int) -> None:
        # Valor Bard 5
        # Warlock 1
        # Valor Bard 19
        base_feats: List[Feat] = []
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

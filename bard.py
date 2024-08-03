from character import Character
from feats import Feat, ASI, AttackAction, DualWielder
from weapons import Weapon, Shortsword, Scimitar
from events import HitArgs, AttackRollArgs
from util import roll_dice, get_magic_weapon
from target import Target
from typing import List
from spells import TrueStrike, HolyWeapon, Spellcaster, EldritchBlast


class TrueStrikeFeat(Feat):
    def __init__(self, level: int) -> None:
        self.name = "TrueStrike"
        if level >= 17:
            self.num_dice = 3
        elif level >= 11:
            self.num_dice = 2
        elif level >= 5:
            self.num_dice = 1
        else:
            self.num_dice = 0

    def roll_attack(self, args: AttackRollArgs):
        if args.attack.has_tag("truestrike"):
            args.situational_bonus += self.character.mod(
                self.character.spell_mod
            ) - self.character.mod(args.attack.weapon.mod)

    def hit(self, args: HitArgs):
        if args.attack.has_tag("truestrike"):
            args.add_damage("TrueStrike", roll_dice(self.num_dice, 6))


class TrueStrikeAction(Feat):
    def __init__(
        self,
        truestrike_weapon: Weapon,
        attacks: List[Weapon],
        nick_attacks: List[Weapon],
    ) -> None:
        self.name = "ValorBardAction"
        self.truestrike_weapon = truestrike_weapon
        self.attacks = attacks
        self.nick_attacks = nick_attacks

    def action(self, target: Target):
        self.character.cast(TrueStrike(self.truestrike_weapon), target)
        for attack in self.attacks:
            self.character.attack(target, attack)
        for attack in self.nick_attacks:
            self.character.attack(target, attack, tags=["light"])


class HolyWeaponFeat(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.name = "HolyWeaponFeat"
        self.weapon = weapon

    def before_action(self, target: Target):
        if not self.character.has_effect("HolyWeapon") and self.character.use_bonus(
            "HolyWeapon"
        ):
            self.character.cast(HolyWeapon(self.character.highest_slot()))

    def hit(self, args: HitArgs):
        if args.attack.weapon.name == self.weapon.name:
            args.add_damage("HolyWeapon", roll_dice(2, 8))


class ValorBardBonusAttack(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.name = "ValorBardBonusAttack"
        self.weapon = weapon

    def after_action(self, target: Target):
        if self.character.use_bonus("ValorBardBonusAttack"):
            self.character.attack(target, self.weapon)


class ValorBard(Character):
    def __init__(self, level: int, **kwargs) -> None:
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        weapon = Shortsword("dex", bonus=magic_weapon)
        scimitar = Scimitar("dex", bonus=magic_weapon)
        base_feats.append(TrueStrikeFeat(level))
        attacks = []
        if level >= 6:
            attacks = [weapon]
        base_feats.append(
            TrueStrikeAction(weapon, attacks=attacks, nick_attacks=[scimitar])
        )
        if level >= 10:
            base_feats.append(HolyWeaponFeat(weapon))
        if level >= 14:
            base_feats.append(ValorBardBonusAttack(weapon))
        feats = [
            ASI([["cha", 2]]),
            ASI([["cha", 1], ["dex", 1]]),
            ASI([["dex", 2]]),
            ASI([["dex", 1]]),
            ASI(),
        ]
        super().init(
            level=level,
            stats=[10, 16, 10, 10, 10, 17],
            base_feats=base_feats,
            feats=feats,
            spellcaster=Spellcaster.FULL,
            spell_mod="cha",
        )


class CMEMulticlassAction(Feat):
    def __init__(self, level: int, weapon: Weapon) -> None:
        super().__init__()
        self.name = "CMEMulticlassAction"
        self.level = level
        self.weapon = weapon

    def action(self, target):
        if self.level >= 7:
            self.character.cast(EldritchBlast(self.level))
        self.character.attack(target, self.weapon)
        self.character.attack(target, self.weapon)


class CMEMulticlass(Character):
    def __init__(self, level: int) -> None:
        # Valor Bard 5
        # Warlock 1
        # Valor Bard 19
        base_feats = []
        weapon = Scimitar()
        base_feats.append(CMEMulticlassAction(level, weapon))
        feats = [
            DualWielder(),
            ASI([["dex", 2]]),
            ASI([["cha", 2]]),
            ASI([["cha", 1]]),
            ASI(),
        ]
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 10, 16],
            base_feats=base_feats,
            feats=feats,
            spellcaster=Spellcaster.FULL,
            spell_mod="cha",
        )

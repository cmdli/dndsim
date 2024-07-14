from events import AttackRollArgs, HitArgs
from target import Target
from util import (
    get_magic_weapon,
    roll_dice,
)
from character import Character
from feats import (
    ASI,
    AttackAction,
    EquipWeapon,
    GreatWeaponMaster,
    Feat,
    TwoWeaponFighting,
)
from weapons import Greatsword, Shortsword, Scimitar
from log import log
from spells import DivineSmite, DivineFavor, Spellcaster


class DivineSmiteFeat(Feat):
    def __init__(self) -> None:
        self.name = "DivineSmite"

    def begin_turn(self, target: Target):
        self.used = False

    def hit(self, args: HitArgs):
        slot = self.character.highest_slot()
        if not self.used and slot >= 1 and self.character.use_bonus("DivineSmite"):
            self.used = True
            self.character.cast(DivineSmite(slot, args.crit), target=args.attack.target)


class ImprovedDivineSmite(Feat):
    def __init__(self, max_reroll: int = 0) -> None:
        self.name = "ImprovedDivineSmite"
        self.max_reroll = max_reroll

    def hit(self, args: HitArgs):
        num = 2 if args.crit else 1
        args.add_damage(
            "ImprovedDivineSmite", roll_dice(num, 8, max_reroll=self.max_reroll)
        )


class SacredWeapon(Feat):
    def __init__(self) -> None:
        self.name = "SacredWeapon"

    def short_rest(self):
        self.enabled = False

    def begin_turn(self, target: Target):
        if not self.enabled and self.character.use_bonus("SacredWeapon"):
            self.enabled = True

    def roll_attack(self, args: AttackRollArgs):
        if self.enabled:
            args.situational_bonus += self.character.mod("cha")


class DivineFavorFeat(Feat):
    def __init__(self) -> None:
        self.name = "DivineFavor"

    def begin_turn(self, target: Target):
        slot = self.character.lowest_slot()
        if (
            not self.character.is_concentrating()
            and slot >= 1
            and self.character.use_bonus("DivineFavor")
        ):
            self.character.cast(DivineFavor(slot))

    def hit(self, args: HitArgs):
        if self.character.concentrating_on("DivineFavor"):
            args.add_damage("DivineFavor", roll_dice(1, 4))


class Paladin(Character):
    def __init__(self, level: int, use_twf=False, **kwargs):
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        if use_twf:
            scimitar = Scimitar("str", bonus=magic_weapon)
            base_feats.append(TwoWeaponFighting())
            base_feats.append(EquipWeapon(scimitar))
            weapon = Shortsword("str", bonus=magic_weapon)
            nick_attacks = [scimitar]
            max_reroll = 0
        else:
            weapon = Greatsword(bonus=magic_weapon)
            nick_attacks = []
            max_reroll = 2
        base_feats.append(EquipWeapon(weapon=weapon, max_reroll=max_reroll))
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(AttackAction(attacks=attacks, nick_attacks=nick_attacks))
        if level >= 2:
            base_feats.append(DivineSmiteFeat())
        if level >= 11:
            base_feats.append(ImprovedDivineSmite())
        if level >= 3:
            base_feats.append(SacredWeapon())
        base_feats.append(DivineFavorFeat())
        if use_twf:
            feats = [
                ASI([["str", 1]]),
                ASI([["str", 2]]),
                ASI([["cha", 2]]),
                ASI([["cha", 2]]),
                ASI(),
            ]
        else:
            feats = [
                GreatWeaponMaster(weapon),
                ASI([["str", 2]]),
                ASI([["cha", 2]]),
                ASI([["cha", 2]]),
                ASI(),
            ]
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 16],
            feats=feats,
            base_feats=base_feats,
            spellcaster=Spellcaster.HALF,
        )

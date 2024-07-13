from character import Character
from events import AttackRollArgs, HitArgs
from feats import Feat, ASI, EquipWeapon, AttackAction
from target import Target
from weapons import Weapon
from util import get_magic_weapon
from fighter import ActionSurge
import random


class OldCrossbowExpert(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.name = "OldCrossbowExpert"
        self.weapon = weapon

    def apply(self, character):
        super().apply(character)
        character.dex += 1

    def end_turn(self, target):
        if self.character.use_bonus("CrossbowExpert"):
            self.character.attack(target, self.weapon)


class OldSharpshooter(Feat):
    def __init__(self) -> None:
        self.name = "OldSharpshooter"

    def apply(self, character):
        super().apply(character)
        character.dex += 1

    def roll_attack(self, args: AttackRollArgs):
        args.situational_bonus -= 5
        args.attack.add_tag("Sharpshooter")

    def hit(self, args: HitArgs):
        if args.attack.has_tag("Sharpshooter"):
            args.add_damage("Sharpshooter", 10)


class FightingSpirit(Feat):
    def __init__(self, regain_on_initiative: bool = False) -> None:
        self.name = "FightingSpirit"
        self.enabled = False
        self.fighting_spirit = 3
        self.regain_on_initiative = regain_on_initiative

    def long_rest(self):
        self.fighting_spirit = 3

    def short_rest(self):
        if self.regain_on_initiative and self.fighting_spirit == 0:
            self.fighting_spirit = 1

    def before_action(self, target: Target):
        if self.fighting_spirit > 0 and self.character.use_bonus("FightingSpirit"):
            self.fighting_spirit -= 1
            self.enabled = True

    def roll_attack(self, args: AttackRollArgs):
        if self.enabled:
            args.adv = True

    def end_turn(self, target):
        self.enabled = False


class RapidStrike(Feat):
    def __init__(self) -> None:
        self.name = "RapidStrike"
        self.used = False

    def begin_turn(self, target: Target):
        self.used = False

    def roll_attack(self, args: AttackRollArgs):
        if not self.used and args.adv and args.attack.has_tag("main_action"):
            self.used = True
            self.character.attack(args.attack.target, args.attack.weapon)


class OldHandCrossbow(Weapon):
    def __init__(self, **kwargs):
        super().__init__(name="OldHandCrossbow", num_dice=1, die=6, mod="dex", **kwargs)


class Blessed(Feat):
    def __init__(self) -> None:
        self.name = "Blessed"

    def roll_attack(self, args: AttackRollArgs):
        args.situational_bonus += random.randint(1, 4)


class AssaultUnit(Character):
    def __init__(self, level: int, blessed: bool = False, **kwargs) -> None:
        magic_weapon = get_magic_weapon(level)
        weapon = OldHandCrossbow(bonus=magic_weapon)
        base_feats = []
        base_feats.append(EquipWeapon(weapon))
        if level >= 20:
            attacks = 4 * [weapon]
        elif level >= 11:
            attacks = 3 * [weapon]
        elif level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(AttackAction(attacks=attacks))
        if level >= 17:
            base_feats.append(ActionSurge(max_surges=2))
        elif level >= 2:
            base_feats.append(ActionSurge(max_surges=1))
        if level >= 10:
            base_feats.append(FightingSpirit(regain_on_initiative=True))
        elif level >= 3:
            base_feats.append(FightingSpirit())
        if level >= 15:
            base_feats.append(RapidStrike())
        if blessed:
            base_feats.append(Blessed())
        feats = [
            OldCrossbowExpert(weapon),
            OldSharpshooter(),
            ASI([["dex", 1]]),
            ASI(),
            ASI(),
            ASI(),
            ASI(),
        ]
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 10, 10],
            base_feats=base_feats,
            feats=feats,
            feat_schedule=[4, 6, 8, 12, 14, 16, 19],
        )

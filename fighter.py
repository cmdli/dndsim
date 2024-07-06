import random
from events import AttackArgs, AttackRollArgs, HitArgs, MissArgs
from target import Target
from util import magic_weapon, roll_dice
from feats import (
    GreatWeaponMaster,
    AttackAction,
    ASI,
    PolearmMaster,
    Feat,
    EquipWeapon,
)
from character import Character
from weapons import Glaive, Greatsword, GlaiveButt, Maul
from log import log


class StudiedAttacks(Feat):
    def __init__(self) -> None:
        self.name = "StudiedAttacks"
        self.enabled = False

    def roll_attack(self, args):
        if self.enabled:
            args.adv = True

    def hit(self, args):
        self.enabled = False

    def miss(self, args):
        self.enabled = True


class HeroicAdvantage(Feat):
    def __init__(self):
        self.name = "HeroicAdvantage"

    def begin_turn(self, target):
        self.used = False

    def roll_attack(self, args):
        if self.used or args.adv:
            return
        if args.disadv:
            roll = min(args.roll1, args.roll2)
            if roll < 8:
                self.used = True
                self.adv = True
                args.roll1 = random.randint(1, 20)
        else:
            roll = args.roll1
            if roll < 8:
                self.used = True
                args.adv = True


class ActionSurge(Feat):
    def __init__(self, max_surges) -> None:
        self.name = "ActionSurge"
        self.max_surges = max_surges

    def apply(self, character):
        self.character = character

    def begin_turn(self, target):
        if self.surges > 0:
            self.character.actions += 1
            self.surges -= 1

    def short_rest(self):
        self.surges = self.max_surges


class PrecisionAttack(Feat):
    def __init__(self, low=5) -> None:
        self.name = "PrecisionAttack"
        self.low = low

    def roll_attack(self, args: AttackRollArgs):
        maneuvers = self.character.feat("Maneuvers")
        if maneuvers.used_maneuver:
            return
        if not args.hits() and args.roll() >= self.low:
            roll = maneuvers.roll()
            args.situational_bonus += roll


class TrippingAttack(Feat):
    def __init__(self) -> None:
        self.name = "TrippingAttack"

    def hit(self, args: HitArgs):
        maneuvers = self.character.feat("Maneuvers")
        if maneuvers.used_maneuver:
            return
        if args.target.prone:
            return
        roll = maneuvers.roll()
        if roll > 0:
            args.add_damage("TrippingAttack", roll)
            if not args.target.save(self.character.dc("str")):
                args.target.prone = True


class Maneuvers(Feat):
    def __init__(self, level) -> None:
        self.name = "Maneuvers"
        if level >= 15:
            self.max_dice = 6
        elif level >= 7:
            self.max_dice = 5
        else:
            self.max_dice = 4
        if level >= 18:
            self.superiority_size = 12
        elif level >= 10:
            self.superiority_size = 10
        else:
            self.superiority_size = 8
        self.enabled_relentless = level >= 15
        self.used_maneuver = False
        self.superiority_dice = 0

    def apply(self, character):
        self.character = character

    def short_rest(self):
        self.superiority_dice = self.max_dice

    def begin_turn(self, target: Target):
        self.used_relentless = False

    def before_attack(self):
        self.used_maneuver = False

    def roll(self):
        if self.superiority_dice > 0:
            self.used_maneuver = True
            self.superiority_dice -= 1
            return roll_dice(1, self.superiority_size)
        elif self.enabled_relentless and self.used_relentless:
            self.used_maneuver = True
            self.used_relentless = True
            return roll_dice(1, 8)
        return 0


class ToppleIfNecessaryAttackAction(Feat):
    def __init__(self, num_attacks, topple_weapon, default_weapon) -> None:
        self.name = "ToppleIfNecessaryAttackAction"
        self.topple_weapon = topple_weapon
        self.default_weapon = default_weapon
        self.num_attacks = num_attacks

    def action(self, target: Target):
        for i in range(self.num_attacks):
            weapon = self.default_weapon
            if not target.prone and i < self.num_attacks - 1:
                weapon = self.topple_weapon
            self.character.attack(target, weapon, main_action=True)


class Fighter(Character):
    def __init__(
        self, level, use_pam=False, subclass_feats=[], min_crit=20, use_topple=True
    ):
        base_feats = []
        self.use_pam = use_pam
        self.magic_weapon = magic_weapon(level)
        if use_pam:
            weapon = Glaive(bonus=self.magic_weapon, min_crit=min_crit)
        else:
            weapon = Greatsword(bonus=self.magic_weapon, min_crit=min_crit)
        base_feats.append(EquipWeapon(weapon, savage_attacker=True, max_reroll=2))
        if level >= 20:
            num_attacks = 4
        elif level >= 11:
            num_attacks = 3
        elif level >= 5:
            num_attacks = 2
        else:
            num_attacks = 1
        if use_topple and level >= 5:
            maul = Maul(bonus=self.magic_weapon, min_crit=min_crit)
            base_feats.append(EquipWeapon(maul, savage_attacker=True, max_reroll=2))
            base_feats.append(ToppleIfNecessaryAttackAction(num_attacks, maul, weapon))
        else:
            base_feats.append(AttackAction(attacks=(num_attacks * [weapon])))
        if level >= 13:
            base_feats.append(StudiedAttacks())
        if level >= 17:
            base_feats.append(ActionSurge(2))
        elif level >= 2:
            base_feats.append(ActionSurge(1))
        base_feats.extend(subclass_feats)
        if use_pam:
            butt = GlaiveButt(bonus=self.magic_weapon, min_crit=min_crit)
            base_feats.append(EquipWeapon(butt, savage_attacker=True, max_reroll=2))
            feats = [
                GreatWeaponMaster(),
                PolearmMaster(butt),
                ASI([["str", 1]]),
                ASI(),
                ASI(),
                ASI(),
                ASI(),
            ]
        else:
            feats = [
                GreatWeaponMaster(),
                ASI([["str", 2]]),
                ASI(),
                ASI(),
                ASI(),
                ASI(),
                ASI(),
            ]
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 10],
            feat_schedule=[4, 6, 8, 12, 14, 16, 19],
            feats=feats,
            base_feats=base_feats,
        )


class ChampionFighter(Fighter):
    def __init__(self, level, **kwargs):
        feats = []
        if level >= 10:
            feats.append(HeroicAdvantage())
        if level >= 15:
            min_crit = 18
        elif level >= 3:
            min_crit = 19
        else:
            min_crit = 20
        super().__init__(
            level,
            subclass_feats=feats,
            min_crit=min_crit,
            **kwargs,
        )


class TrippingFighter(Fighter):
    def __init__(self, level, **kwargs):
        feats = []
        if level >= 3:
            feats.append(Maneuvers(level))
            feats.append(TrippingAttack())
        super().__init__(level, subclass_feats=feats, **kwargs)


class BattlemasterFighter(Fighter):
    def __init__(self, level, **kwargs):
        feats = []
        if level >= 3:
            feats.append(Maneuvers(level))
        super().__init__(level, subclass_feats=feats, **kwargs)


class PrecisionFighter(Fighter):
    def __init__(self, level, low=8, **kwargs):
        feats = []
        if level >= 3:
            feats.append(Maneuvers(level))
            feats.append(PrecisionAttack(low=low))
        super().__init__(level, subclass_feats=feats, **kwargs)


class PrecisionTrippingFighter(Fighter):
    def __init__(self, level, low=1, **kwargs):
        feats = []
        if level >= 3:
            feats.append(Maneuvers(level))
            feats.append(TrippingAttack())
            feats.append(PrecisionAttack(low=low))
        super().__init__(level, subclass_feats=feats, **kwargs)

import random
from typing import List, Optional

from util.util import get_magic_weapon
from feats import (
    GreatWeaponMaster,
    AttackAction,
    ASI,
    PolearmMaster,
    IrresistibleOffense,
    TwoWeaponFighting,
    WeaponMasteries,
    DualWielder,
    SavageAttacker,
    GreatWeaponFighting,
)
from weapons import (
    Glaive,
    Greatsword,
    GlaiveButt,
    Maul,
    Shortsword,
    Scimitar,
    Rapier,
)

import sim.feat
import sim.weapons
import sim.character
import sim.target


def get_num_attacks(level: int):
    if level >= 20:
        return 4
    elif level >= 11:
        return 3
    elif level >= 5:
        return 2
    else:
        return 1


class StudiedAttacks(sim.feat.Feat):
    def __init__(self) -> None:
        self.enabled = False

    def attack_roll(self, args):
        if self.enabled:
            args.adv = True
            self.enabled = False

    def attack_result(self, args):
        if args.misses():
            self.enabled = True


class HeroicAdvantage(sim.feat.Feat):
    def begin_turn(self, target):
        self.used = False

    def attack_roll(self, args):
        if self.used or args.adv:
            return
        if args.disadv:
            roll = args.roll()
            if roll < 8:
                self.used = True
                self.adv = True
                args.roll1 = random.randint(1, 20)
        else:
            roll = args.roll1
            if roll < 8:
                self.used = True
                args.adv = True


class ActionSurge(sim.feat.Feat):
    def __init__(self, max_surges) -> None:
        self.max_surges = max_surges

    def before_action(self, target):
        if self.surges > 0:
            self.character.actions += 1
            self.surges -= 1

    def short_rest(self):
        self.surges = self.max_surges


class PrecisionAttack(sim.feat.Feat):
    def __init__(self, low=5) -> None:
        self.low = low

    def attack_roll(self, args):
        if args.attack.has_tag("used_maneuver"):
            return
        if not args.hits() and args.roll() >= self.low:
            roll = self.character.maneuvers.roll()
            args.situational_bonus += roll
            args.attack.add_tag("used_maneuver")


class TrippingAttack(sim.feat.Feat):
    def attack_result(self, args):
        if args.misses():
            return
        if args.attack.has_tag("used_maneuver"):
            return
        if args.attack.target.prone:
            return
        die = self.character.maneuvers.use()
        if die > 0:
            args.add_damage(source="TrippingAttack", dice=[die])
            if not args.attack.target.save(self.character.dc("str")):
                args.attack.target.knock_prone()
            args.attack.add_tag("used_maneuver")


class CombatSuperiority(sim.feat.Feat):
    def __init__(self, level) -> None:
        super().__init__()
        self.level = level

    def apply(self, character):
        if self.level >= 15:
            character.maneuvers.max_dice = 6
        elif self.level >= 7:
            character.maneuvers.max_dice = 5
        else:
            character.maneuvers.max_dice = 4
        if self.level >= 18:
            character.maneuvers.die = 12
        elif self.level >= 10:
            character.maneuvers.die = 10
        else:
            character.maneuvers.die = 8


class Relentless(sim.feat.Feat):
    def apply(self, character):
        character.maneuvers.relentless = True


class ToppleIfNecessaryAttackAction(sim.feat.Feat):
    def __init__(self, num_attacks, topple_weapon, default_weapon) -> None:
        self.topple_weapon = topple_weapon
        self.default_weapon = default_weapon
        self.num_attacks = num_attacks

    def action(self, target: "sim.target.Target"):
        for i in range(self.num_attacks):
            weapon = self.default_weapon
            if not target.prone and i < self.num_attacks - 1:
                weapon = self.topple_weapon
            self.character.weapon_attack(target, weapon, tags=["main_action"])


class ImprovedCritical(sim.feat.Feat):
    def __init__(self, min_crit: int):
        self.min_crit = min_crit

    def attack_roll(self, args):
        if args.min_crit:
            args.min_crit = min(args.min_crit, self.min_crit)
        else:
            args.min_crit = self.min_crit


class DefaultFighterAction(sim.feat.Feat):
    def __init__(
        self,
        level: int,
        weapon: "sim.weapons.Weapon",
        topple_weapon: Optional["sim.weapons.Weapon"] = None,
        nick_weapon: Optional["sim.weapons.Weapon"] = None,
    ):
        self.num_attacks = get_num_attacks(level)
        self.weapon = weapon
        self.topple_weapon = topple_weapon
        self.nick_weapon = nick_weapon

    def action(self, target: "sim.target.Target"):
        for i in range(self.num_attacks):
            weapon = self.weapon
            if (
                self.topple_weapon is not None
                and not target.prone
                and i < self.num_attacks - 1
            ):
                weapon = self.topple_weapon
            self.character.weapon_attack(target, weapon, tags=["main_action"])
        if self.nick_weapon:
            self.character.weapon_attack(
                target, self.nick_weapon, tags=["main_action", "light"]
            )


def fighter_feats(
    level: int,
    masteries: List["sim.weapons.WeaponMastery"],
    fighting_style: "sim.feat.Feat",
) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    # Level 1 (Second Wind) is irrelevant
    feats.append(WeaponMasteries(masteries))
    feats.append(fighting_style)
    if level >= 2:
        feats.append(ActionSurge(2 if level >= 17 else 1))
    # Level 2 (Tactical Mind) is irrelevant
    # Level 5 (Extra Attack) is handled in the attack action
    # Level 5 (Tactical Shift) is irrelevant
    # Level 9 (Indomitable) is irrelevant
    # Level 9 (Tactical Master) is irrelevant currently
    # Level 11 (Extra Attack 2) is handled in the attack action
    if level >= 13:
        feats.append(StudiedAttacks())
    # Level 20 (Extra Attack 3) is handled in the attack action
    return feats


def champion_feats(level: int) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 3:
        feats.append(ImprovedCritical(18 if level >= 15 else 19))
    # Level 3 (Remarkable Athlete) is irrelevant
    # Level 7 (Additional Fighting Style) is irrelevant currently
    if level >= 10:
        feats.append(HeroicAdvantage())
    # Level 18 (Survivor) is irrelevant
    return feats


def battlemaster_feats(level: int) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 3:
        feats.append(CombatSuperiority(level))
    if level >= 15:
        feats.append(Relentless())
    return feats


class Fighter(sim.character.Character):
    def __init__(
        self, level: int, use_pam=False, subclass_feats=[], use_topple=True, **kwargs
    ):
        feats: List["sim.feat.Feat"] = []

        # Weapon
        magic_weapon = get_magic_weapon(level)
        if use_pam:
            weapon: "sim.weapons.Weapon" = Glaive(magic_bonus=magic_weapon)
        else:
            weapon = Greatsword(magic_bonus=magic_weapon)

        # Action
        maul = Maul(magic_bonus=magic_weapon)
        feats.append(DefaultFighterAction(level, weapon, maul if use_topple else None))

        # Normal Feats
        feats.append(SavageAttacker())
        if level >= 4:
            feats.append(GreatWeaponMaster(weapon))
        if level >= 6:
            if use_pam:
                butt = GlaiveButt(bonus=magic_weapon)
                feats.append(PolearmMaster(butt))
            else:
                feats.append(ASI(["str"]))
        if level >= 8:
            feats.append(ASI(["str"]))
        if level >= 19:
            feats.append(IrresistibleOffense("str"))

        # Standard feats
        feats.extend(subclass_feats)
        feats.extend(
            fighter_feats(
                level,
                masteries=["Topple", "Graze"],
                fighting_style=GreatWeaponFighting(),
            )
        )
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 10],
            base_feats=feats,
        )


class ChampionFighter(Fighter):
    def __init__(self, level: int, **kwargs):
        super().__init__(
            level,
            subclass_feats=champion_feats(level),
            **kwargs,
        )


class TrippingFighter(Fighter):
    def __init__(self, level: int, **kwargs):
        feats: List["sim.feat.Feat"] = []
        feats.append(TrippingAttack())
        feats.extend(battlemaster_feats(level))
        super().__init__(level, subclass_feats=feats, **kwargs)


class BattlemasterFighter(Fighter):
    def __init__(self, level: int, **kwargs):
        feats: List["sim.feat.Feat"] = []
        feats.extend(battlemaster_feats(level))
        super().__init__(level, subclass_feats=feats, **kwargs)


class PrecisionFighter(Fighter):
    def __init__(self, level: int, low: int = 8, **kwargs):
        feats: List[sim.feat.Feat] = []
        feats.append(PrecisionAttack(low=low))
        feats.extend(battlemaster_feats(level))
        super().__init__(level, subclass_feats=feats, **kwargs)


class PrecisionTrippingFighter(Fighter):
    def __init__(self, level: int, low: int = 1, **kwargs):
        feats: List["sim.feat.Feat"] = []
        feats.append(TrippingAttack())
        feats.append(PrecisionAttack(low=low))
        feats.extend(battlemaster_feats(level))
        super().__init__(level, subclass_feats=feats, **kwargs)


class TWFFighter(sim.character.Character):
    def __init__(self, level: int, **kwargs) -> None:
        magic_weapon = get_magic_weapon(level)
        feats: List["sim.feat.Feat"] = []
        if level >= 6:
            weapon: "sim.weapons.Weapon" = Rapier(magic_bonus=magic_weapon)
        else:
            weapon = Shortsword(magic_bonus=magic_weapon)
        scimitar = Scimitar(magic_bonus=magic_weapon)
        feats.append(DefaultFighterAction(level, weapon, nick_weapon=scimitar))
        feats.append(SavageAttacker())
        if level >= 4:
            feats.append(GreatWeaponMaster(weapon))
        if level >= 6:
            feats.append(DualWielder("str", weapon))
        if level >= 8:
            feats.append(ASI(["str"]))
        if level >= 19:
            feats.append(IrresistibleOffense("str"))
        feats.extend(
            fighter_feats(
                level,
                masteries=["Vex", "Nick"],
                fighting_style=TwoWeaponFighting(),
            )
        )
        feats.extend(champion_feats(level))
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 10],
            base_feats=feats,
        )

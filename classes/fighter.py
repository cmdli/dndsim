import random
from typing import List

from util.util import get_magic_weapon, roll_dice
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
from sim.weapons import (
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
        maneuvers = self.character.feat("Maneuvers")
        if not args.hits() and args.roll() >= self.low:
            roll = maneuvers.roll()
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
        maneuvers = self.character.feat("Maneuvers")
        die = maneuvers.use()
        if die > 0:
            args.add_damage(source="TrippingAttack", dice=[die])
            if not args.attack.target.save(self.character.dc("str")):
                args.attack.target.knock_prone()
            args.attack.add_tag("used_maneuver")


class Maneuvers(sim.feat.Feat):
    def __init__(self, level) -> None:
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
        self.superiority_dice = 0

    def short_rest(self):
        self.superiority_dice = self.max_dice

    def begin_turn(self, target: "sim.target.Target"):
        self.used_relentless = False

    def use(self):
        if self.superiority_dice > 0:
            self.superiority_dice -= 1
            return self.superiority_size
        elif self.enabled_relentless and self.used_relentless:
            self.used_relentless = True
            return 8
        return 0

    def roll(self):
        die = self.use()
        if die > 0:
            return roll_dice(1, die)
        return 0


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


class Fighter(sim.character.Character):
    def __init__(
        self,
        level: int,
        use_pam=False,
        subclass_feats=[],
        min_crit=20,
        use_topple=True,
        **kwargs
    ):
        magic_weapon = get_magic_weapon(level)
        if use_pam:
            weapon: "sim.weapons.Weapon" = Glaive(
                magic_bonus=magic_weapon, min_crit=min_crit
            )
        else:
            weapon = Greatsword(magic_bonus=magic_weapon, min_crit=min_crit)
        if level >= 20:
            num_attacks = 4
        elif level >= 11:
            num_attacks = 3
        elif level >= 5:
            num_attacks = 2
        else:
            num_attacks = 1
        base_feats: List["sim.feat.Feat"] = []
        base_feats.append(WeaponMasteries(["Topple", "Graze"]))
        base_feats.append(SavageAttacker())
        base_feats.append(GreatWeaponFighting())
        if use_topple and level >= 5:
            maul = Maul(magic_bonus=magic_weapon, min_crit=min_crit)
            base_feats.append(ToppleIfNecessaryAttackAction(num_attacks, maul, weapon))
        else:
            base_feats.append(AttackAction(attacks=(num_attacks * [weapon])))
        if level >= 2:
            base_feats.append(ActionSurge(2 if level >= 17 else 1))
        if level >= 4:
            base_feats.append(GreatWeaponMaster(weapon))
        if level >= 6:
            if use_pam:
                butt = GlaiveButt(bonus=magic_weapon, min_crit=min_crit)
                base_feats.append(PolearmMaster(butt))
            else:
                base_feats.append(ASI(["str"]))
        if level >= 13:
            base_feats.append(StudiedAttacks())
        if level >= 19:
            base_feats.append(IrresistibleOffense("str"))
        base_feats.extend(subclass_feats)
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 10],
            base_feats=base_feats,
        )


class ChampionFighter(Fighter):
    def __init__(self, level: int, **kwargs):
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
    def __init__(self, level: int, **kwargs):
        feats: List["sim.feat.Feat"] = []
        if level >= 3:
            feats.append(Maneuvers(level))
            feats.append(TrippingAttack())
        super().__init__(level, subclass_feats=feats, **kwargs)


class BattlemasterFighter(Fighter):
    def __init__(self, level: int, **kwargs):
        feats: List["sim.feat.Feat"] = []
        if level >= 3:
            feats.append(Maneuvers(level))
        super().__init__(level, subclass_feats=feats, **kwargs)


class PrecisionFighter(Fighter):
    def __init__(self, level: int, low: int = 8, **kwargs):
        feats: List[sim.feat.Feat] = []
        if level >= 3:
            feats.append(Maneuvers(level))
            feats.append(PrecisionAttack(low=low))
        super().__init__(level, subclass_feats=feats, **kwargs)


class PrecisionTrippingFighter(Fighter):
    def __init__(self, level: int, low: int = 1, **kwargs):
        feats: List["sim.feat.Feat"] = []
        if level >= 3:
            feats.append(Maneuvers(level))
            feats.append(TrippingAttack())
            feats.append(PrecisionAttack(low=low))
        super().__init__(level, subclass_feats=feats, **kwargs)


class TWFFighter(sim.character.Character):
    def __init__(self, level: int, **kwargs) -> None:
        if level >= 15:
            min_crit = 18
        elif level >= 3:
            min_crit = 19
        else:
            min_crit = 20
        magic_weapon = get_magic_weapon(level)
        base_feats: List["sim.feat.Feat"] = []
        base_feats.append(WeaponMasteries(["Vex", "Nick"]))
        base_feats.append(TwoWeaponFighting())
        base_feats.append(SavageAttacker())
        if level >= 6:
            weapon: "sim.weapons.Weapon" = Rapier(
                magic_bonus=magic_weapon, min_crit=min_crit
            )
        else:
            weapon = Shortsword(magic_bonus=magic_weapon, min_crit=min_crit)
        scimitar = Scimitar(magic_bonus=magic_weapon, min_crit=min_crit)
        num_attacks = get_num_attacks(level)
        base_feats.append(
            AttackAction(attacks=(num_attacks * [weapon]), nick_attacks=[scimitar])
        )
        if level >= 2:
            base_feats.append(ActionSurge(2 if level >= 17 else 1))
        if level >= 4:
            base_feats.append(GreatWeaponMaster(weapon))
        if level >= 6:
            base_feats.append(DualWielder("str", weapon))
        if level >= 8:
            base_feats.append(ASI(["str"]))
        if level >= 10:
            base_feats.append(HeroicAdvantage())
        if level >= 13:
            base_feats.append(StudiedAttacks())
        if level >= 19:
            base_feats.append(IrresistibleOffense("str"))
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 10],
            base_feats=base_feats,
        )

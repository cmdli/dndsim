from util.util import get_magic_weapon, roll_dice
from sim.character import Character
from sim.feats import (
    ASI,
    AttackAction,
    Feat,
    IrresistibleOffense,
    WeaponMaster,
)
from sim.weapons import Weapon
from sim.events import HitArgs, WeaponRollArgs
from sim.target import Target
from util.log import log


def martial_arts_die(level: int):
    if level >= 17:
        return 12
    elif level >= 11:
        return 10
    elif level >= 5:
        return 8
    else:
        return 6


class BodyAndMind(Feat):
    def apply(self, character):
        super().apply(character)
        character.dex += 4
        character.wis += 4


class FlurryOfBlows(Feat):
    def __init__(self, num_attacks, weapon):
        self.num_attacks = num_attacks
        self.weapon = weapon

    def before_action(self, target: Target):
        if self.character.ki > 0 and self.character.use_bonus("FlurryOfBlows"):
            self.character.ki -= 1
            for _ in range(self.num_attacks):
                self.character.attack(target, self.weapon, tags=["flurry"])
        elif self.character.use_bonus("BonusAttack"):
            self.character.attack(target, self.weapon)


class OpenHandTechnique(Feat):
    def hit(self, args: HitArgs):
        if args.attack.has_tag("flurry"):
            if not args.attack.target.save(self.character.dc("wis")):
                log.record("Knocked prone", 1)
                args.attack.target.prone = True


class Grappler(Feat):
    def apply(self, character):
        super().apply(character)
        character.dex += 1

    def hit(self, args: HitArgs):
        if args.attack.has_tag("main_action"):
            args.attack.target.grapple()

    def roll_attack(self, args):
        if args.attack.target.grappled:
            args.adv = True


class StunningStrike(Feat):
    def __init__(self, weapon_die, avoid_on_grapple: bool = False):
        self.weapon_die = weapon_die
        self.stuns = []
        self.avoid_on_grapple = avoid_on_grapple

    def begin_turn(self, target: Target):
        self.used = False
        target.stunned = False

    def hit(self, args: HitArgs):
        if self.used or self.character.ki == 0:
            return
        if args.attack.target.grappled and self.avoid_on_grapple:
            return
        if args.attack.target.stunned:
            return
        self.used = True
        self.character.ki -= 1
        if not args.attack.target.save(self.character.dc("wis")):
            args.attack.target.stunned = True
        else:
            args.attack.target.semistunned = True


class Ki(Feat):
    def __init__(self, max_ki):
        self.max_ki = max_ki

    def short_rest(self):
        self.character.ki = self.max_ki


class Fists(Weapon):
    def __init__(self, weapon_die, bonus=0):
        super().__init__(
            name="Fists",
            num_dice=1,
            die=weapon_die,
            magic_bonus=bonus,
            tags=["finesse"],
        )


class MagicInitiateHuntersMark(Feat):
    def __init__(self) -> None:
        self.enabled = False
        self.used = False

    def long_rest(self):
        self.used = False

    def short_rest(self):
        self.enabled = False

    def before_action(self, target: Target):
        if not self.used and self.character.use_bonus("HuntersMark"):
            self.used = True
            self.enabled = True

    def hit(self, args: HitArgs):
        if self.enabled:
            args.add_damage("HuntersMark", roll_dice(1, 6))


class TavernBrawler(Feat):
    def __init__(self, die: int) -> None:
        self.die = die

    def weapon_roll(self, args: WeaponRollArgs):
        for i in range(len(args.rolls)):
            if args.rolls[i] == 1:
                args.rolls[i] = roll_dice(1, self.die)


class Monk(Character):
    def __init__(
        self, level, use_nick: bool = False, use_grappler: bool = True, **kwargs
    ):
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        weapon_die = martial_arts_die(level)
        base_feats.append(TavernBrawler(weapon_die))
        fists = Fists(weapon_die, bonus=magic_weapon)
        weapon = fists
        nick_attacks = []
        if use_nick and level >= 8:
            # Using fists here to simulate a monk weapon
            nick_attacks = [fists]
        num_attacks = 2 if level >= 5 else 1
        base_feats.append(
            AttackAction(attacks=(num_attacks * [weapon]), nick_attacks=nick_attacks)
        )
        base_feats.append(Ki(level if level >= 2 else 0))
        if level >= 10:
            bonus_attacks = 3
        elif level >= 2:
            bonus_attacks = 2
        else:
            bonus_attacks = 0
        base_feats.append(FlurryOfBlows(num_attacks=bonus_attacks, weapon=fists))
        if level >= 3:
            base_feats.append(OpenHandTechnique())
        if level >= 4:
            if use_nick:
                base_feats.append(WeaponMaster("dex"))
            else:
                base_feats.append(Grappler() if use_grappler else ASI(["dex", "con"]))
        if level >= 5:
            base_feats.append(StunningStrike(weapon_die, avoid_on_grapple=not use_nick))
        if level >= 8:
            base_feats.append(ASI(["dex"]))
        if level >= 12:
            base_feats.append(ASI(["wis"]))
        if level >= 16:
            base_feats.append(ASI(["wis"]))
        if level >= 19:
            base_feats.append(IrresistibleOffense("dex"))
        if level >= 20:
            base_feats.append(BodyAndMind())
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            base_feats=base_feats,
        )

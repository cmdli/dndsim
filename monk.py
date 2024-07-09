import random
from util import get_magic_weapon, roll_dice
from character import Character
from feats import ASI, AttackAction, Feat, EquipWeapon, IrresistibleOffense
from weapons import Weapon, Quarterstaff
from events import HitArgs
from target import Target


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
    def __init__(self):
        self.name = "BodyAndMind"

    def apply(self, character):
        super().apply(character)
        character.dex += 4
        character.wis += 4


class FlurryOfBlows(Feat):
    def __init__(self, num_attacks, weapon):
        self.name = "FlurryOfBlows"
        self.num_attacks = num_attacks
        self.weapon = weapon

    def after_action(self, target):
        if self.character.ki > 0 and self.character.use_bonus("FlurryOfBlows"):
            self.character.ki -= 1
            for _ in range(self.num_attacks):
                self.character.attack(target, self.weapon)
        elif self.character.use_bonus("BonusAttack"):
            self.character.attack(target, self.weapon)


class Grappler(Feat):
    def __init__(self):
        self.name = "Grappler"

    def apply(self, character):
        super().apply(character)
        character.dex += 1

    def hit(self, args):
        if args.attack.has_tag("main_action"):
            args.attack.target.grapple()

    def roll_attack(self, args):
        if args.attack.target.grappled:
            args.adv = True


class StunningStrike(Feat):
    def __init__(self, weapon_die):
        self.name = "StunningStrike"
        self.weapon_die = weapon_die
        self.stuns = []

    def begin_turn(self, target):
        self.used = False

    def hit(self, args: HitArgs):
        if not self.used and self.character.ki > 0:
            self.used = True
            self.character.ki -= 1
            if not args.attack.target.save(self.character.dc("wis")):
                args.attack.target.stunned = True
                self.stuns.append(1)
            else:
                args.attack.target.semistunned = True

    def end_turn(self, target: Target):
        self.stuns = [stun - 1 for stun in self.stuns if stun > 0]
        if len(self.stuns) == 0:
            target.stunned = False


class Ki(Feat):
    def __init__(self, max_ki):
        self.name = "Ki"
        self.max_ki = max_ki

    def short_rest(self):
        self.character.ki = self.max_ki


class Fists(Weapon):
    def __init__(self, weapon_die, bonus=0):
        super().__init__(
            name="Fists", num_dice=1, die=weapon_die, mod="dex", bonus=bonus
        )


class Monk(Character):
    def __init__(self, level):
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        weapon_die = martial_arts_die(level)
        fists = Fists(weapon_die, bonus=magic_weapon)
        weapon = fists
        base_feats.append(EquipWeapon(weapon=weapon, max_reroll=1))
        num_attacks = 2 if level >= 5 else 1
        base_feats.append(AttackAction(attacks=(num_attacks * [weapon])))
        base_feats.append(Ki(level if level >= 2 else 0))
        if level >= 10:
            bonus_attacks = 3
        elif level >= 2:
            bonus_attacks = 2
        else:
            bonus_attacks = 0
        base_feats.append(FlurryOfBlows(num_attacks=bonus_attacks, weapon=fists))
        if level >= 5:
            base_feats.append(StunningStrike(weapon_die))
        if level >= 20:
            base_feats.append(BodyAndMind())
        feats = [
            Grappler(),
            ASI([["dex", 2]]),
            ASI([["wis", 2]]),
            ASI([["wis", 2]]),
            IrresistibleOffense("dex"),
        ]
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            base_feats=base_feats,
            feats=feats,
        )

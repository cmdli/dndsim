import random
from util import magic_weapon, roll_dice
from character import Character
from feats import ASI, AttackAction, Feat, EquipWeapon
from weapons import Weapon


class BodyAndMind(Feat):
    def __init__(self):
        self.name = "BodyAndMind"

    def apply(self, character):
        character.dex += 4
        character.wis += 4


class FlurryOfBlows(Feat):
    def __init__(self, num_attacks, weapon):
        self.name = "FlurryOfBlows"
        self.num_attacks = num_attacks
        self.weapon = weapon

    def apply(self, character):
        self.character = character

    def end_turn(self, target):
        if self.character.ki > 0 and self.character.use_bonus("FlurryOfBlows"):
            self.character.ki -= 1
            for _ in range(self.num_attacks):
                self.character.attack(target, self.weapon)


class BonusAttack(Feat):
    def __init__(self, weapon):
        self.name = "BonusAttack"
        self.weapon = weapon

    def apply(self, character):
        self.character = character

    def end_turn(self, target):
        if self.character.use_bonus("BonusAttack"):
            self.character.attack(target, self.weapon)


class Grappler(Feat):
    def __init__(self):
        self.name = "Grappler"

    def apply(self, character):
        character.dex += 1

    def hit(self, args):
        if args.main_action:
            args.target.grapple()

    def roll_attack(self, args):
        if args.target.grappled:
            args.adv = True


class StunningStrike(Feat):
    def __init__(self, weapon_die):
        self.name = "StunningStrike"
        self.weapon_die = weapon_die

    def apply(self, character):
        self.character = character

    def begin_turn(self, target):
        self.used = False

    def roll_attack(self, args):
        if args.target.stunned:
            args.adv = True

    def hit(self, args):
        if not self.used and self.character.ki > 0:
            self.used = True
            self.character.ki -= 1
            if not args.target.save(self.character.dc("wis")):
                args.target.stun()
            else:
                args.add_damage(
                    "StunningStrike",
                    roll_dice(1, self.weapon_die) + self.character.mod("wis"),
                )


class Ki(Feat):
    def __init__(self, max_ki):
        self.name = "Ki"
        self.max_ki = max_ki

    def apply(self, character):
        self.character = character

    def short_rest(self):
        self.character.ki = self.max_ki


class Fists(Weapon):
    def __init__(self, weapon_die, bonus=0):
        super().__init__(
            name="Fists", num_dice=1, die=weapon_die, mod="dex", bonus=bonus
        )


class Monk(Character):
    def __init__(self, level):
        self.magic_weapon = magic_weapon(level)
        base_feats = []
        if level >= 17:
            weapon_die = 12
        elif level >= 11:
            weapon_die = 10
        elif level >= 5:
            weapon_die = 8
        else:
            weapon_die = 6
        fists = Fists(weapon_die, bonus=self.magic_weapon)
        base_feats.append(EquipWeapon(weapon=fists, max_reroll=1))
        if level >= 5:
            attacks = 2 * [fists]
        else:
            attacks = [fists]
        base_feats.append(AttackAction(attacks=attacks))
        if level >= 10:
            base_feats.append(FlurryOfBlows(num_attacks=3, weapon=fists))
        elif level >= 2:
            base_feats.append(FlurryOfBlows(num_attacks=2, weapon=fists))
        base_feats.append(BonusAttack(weapon=fists))
        base_feats.append(Ki(level if level >= 2 else 0))
        if level >= 5:
            base_feats.append(StunningStrike(weapon_die))
        if level >= 20:
            base_feats.append(BodyAndMind())
        feats = [
            Grappler(),
            ASI([["dex", 2]]),
            ASI([["wis", 2]]),
            ASI([["wis", 2]]),
            ASI(),
        ]
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            base_feats=base_feats,
            feats=feats,
        )

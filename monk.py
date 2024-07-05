import random
from util import magic_weapon, do_roll, roll_dice
from character import Character, Feat
from feats import ASI, AttackAction, Attack, Weapon


class BodyAndMind(Feat):
    def __init__(self):
        self.name = "BodyAndMind"

    def apply(self, character):
        character.dex += 4
        character.wis += 4


class FlurryOfBlows(Feat):
    def __init__(self, num_attacks):
        self.name = "FlurryOfBlows"
        self.num_attacks = num_attacks

    def apply(self, character):
        self.character = character

    def end_turn(self, target, **kwargs):
        if not self.character.used_bonus and self.character.ki > 0:
            self.character.used_bonus = True
            self.character.ki -= 1
            for _ in range(self.num_attacks):
                self.character.attack(target)


class BonusAttack(Feat):
    def __init__(self):
        self.name = "BonusAttack"

    def apply(self, character):
        self.character = character

    def end_turn(self, target, **kwargs):
        if not self.character.used_bonus:
            self.character.used_bonus = True
            self.character.attack(target)


class Grappler(Feat):
    def __init__(self):
        self.name = "Grappler"

    def apply(self, character):
        character.dex += 1

    def hit(self, target, main_action=False, **kwargs):
        if main_action:
            target.grapple()

    def roll_attack(self, args, **kwargs):
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

    def roll_attack(self, args, **kwargs):
        if args.target.stunned:
            args.adv = True

    def hit(self, target, **kwargs):
        global stun
        if not self.used and self.character.ki > 0:
            self.used = True
            self.character.ki -= 1
            if not target.save(self.character.dc("wis")):
                target.stun()
            else:
                target.damage(roll_dice(1, self.weapon_die) + self.character.mod("wis"))


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
            num_dice=1, size=weapon_die, mod="dex", bonus=bonus, max_reroll=1
        )


class Monk(Character):
    def __init__(self, level):
        self.magic_weapon = magic_weapon(level)
        base_feats = []
        if level >= 20:
            base_feats.append(BodyAndMind())
        if level >= 17:
            weapon_die = 12
        elif level >= 11:
            weapon_die = 10
        elif level >= 5:
            weapon_die = 8
        else:
            weapon_die = 6
        base_feats.append(Fists(weapon_die, bonus=self.magic_weapon))
        base_feats.append(Attack(mod="dex", bonus=self.magic_weapon))
        if level >= 5:
            base_feats.append(AttackAction(2))
        else:
            base_feats.append(AttackAction(1))
        if level >= 10:
            base_feats.append(FlurryOfBlows(3))
        elif level >= 2:
            base_feats.append(FlurryOfBlows(2))
        base_feats.append(BonusAttack())
        if level >= 5:
            base_feats.append(StunningStrike(weapon_die))
        base_feats.append(Ki(level if level >= 2 else 0))
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
        print(self.dc("wis"))

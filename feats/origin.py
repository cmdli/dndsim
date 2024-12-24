from util.util import roll_dice

import sim.feat


class SavageAttacker(sim.feat.Feat):
    def __init__(self) -> None:
        self.used = False

    def begin_turn(self, target):
        self.used = False

    def damage_roll(self, args):
        if self.used or not args.attack.weapon:
            return
        self.used = True
        new_rolls = [roll_dice(1, die) for die in args.damage.dice]
        if sum(new_rolls) > sum(args.damage.rolls):
            args.damage.rolls = new_rolls


class TavernBrawler(sim.feat.Feat):
    def damage_roll(self, args):
        for i in range(len(args.damage.rolls)):
            if args.damage.rolls[i] == 1:
                args.damage.rolls[i] = roll_dice(1, args.damage.dice[i])

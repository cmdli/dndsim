from util.util import roll_dice

import sim.feat


class Maneuvers:
    def __init__(self) -> None:
        self.max_dice = 0
        self.die = 0
        self.relentless = False
        self.dice = 0
        self.used_relentless = False

    def short_rest(self):
        self.dice = self.max_dice

    def begin_turn(self, target: "sim.target.Target"):
        self.used_relentless = False

    def use(self):
        if self.dice > 0:
            self.dice -= 1
            return self.die
        elif self.relentless and not self.used_relentless:
            self.used_relentless = True
            return 8
        return 0

    def roll(self):
        die = self.use()
        if die > 0:
            return roll_dice(1, die)
        return 0

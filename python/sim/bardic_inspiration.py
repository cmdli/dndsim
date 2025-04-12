from util.util import roll_dice

import sim.character


class BardicInspiration:
    def __init__(self, character: "sim.character.Character"):
        self.die = 0
        self.num = 0

    def use(self):
        if self.num == 0:
            return 0
        self.num -= 1
        return roll_dice(1, self.die)

import sim.character
import sim.event_loop


class Resource(sim.event_loop.Listener):
    def __init__(self, character: "sim.character.Character", short_rest: bool = False):
        self.num = 0
        self.max = 0
        if short_rest:
            character.events.add(self, "short_rest")
        else:
            character.events.add(self, "long_rest")

    def increase_max(self, amount: int):
        self.max += amount

    def short_rest(self):
        self.reset()

    def long_rest(self):
        self.reset()

    def reset(self):
        self.num = self.max

    def use(self):
        if self.num > 0:
            self.num -= 1
            return True
        return False

    def has(self):
        return self.num > 0
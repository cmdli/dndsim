import sim.character
import sim.target
import sim.events

EVENT_NAMES = set(
    [
        "begin_turn",
        "before_action",
        "action",
        "after_action",
        "before_attack",
        "attack",
        "roll_attack",
        "hit",
        "miss",
        "end_turn",
        "enemy_turn",
        "short_rest",
        "long_rest",
        "weapon_roll",
    ]
)


class Feat:
    def __init__(self) -> None:
        self.name: str = None

    def apply(self, character: "sim.character.Character"):
        self.character = character

    def events(self):
        global EVENT_NAMES
        events = []
        for name in self.__dir__():
            if name in EVENT_NAMES and getattr(type(self), name) != getattr(Feat, name):
                events.append(name)
        return events

    def begin_turn(self, target: "sim.target.Target"):
        pass

    def end_turn(self, target: "sim.target.Target"):
        pass

    def before_action(self, target: "sim.target.Target"):
        pass

    def action(self, target: "sim.target.Target"):
        pass

    def after_action(self, target: "sim.target.Target"):
        pass

    def before_attack(self):
        pass

    def attack(self, args: "sim.events.AttackArgs"):
        pass

    def roll_attack(self, args: "sim.events.AttackRollArgs"):
        pass

    def weapon_roll(self, args: "sim.events.WeaponRollArgs"):
        pass

    def hit(self, args: "sim.events.HitArgs"):
        pass

    def miss(self, args: "sim.events.MissArgs"):
        pass

    def enemy_turn(self, target: "sim.target.Target"):
        pass

    def short_rest(self):
        pass

    def long_rest(self):
        pass

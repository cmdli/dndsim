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
        "attack_result",
        "end_turn",
        "enemy_turn",
        "short_rest",
        "long_rest",
        "weapon_roll",
        "cast_spell",
        "damage_roll",
    ]
)


class Feat:
    def name(self) -> str:
        return type(self).__name__

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

    def attack_result(self, args: "sim.events.AttackResultArgs"):
        pass

    def enemy_turn(self, target: "sim.target.Target"):
        pass

    def short_rest(self):
        pass

    def long_rest(self):
        pass

    def cast_spell(self, args: "sim.events.CastSpellArgs"):
        pass

    def damage_roll(self, args: "sim.events.DamageRollArgs"):
        pass

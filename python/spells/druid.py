from sim.character import Character

import sim.event_loop
import sim.spells
import sim.target
import sim.events


class ConjureMinorElementals(sim.event_loop.Listener, sim.spells.Spell):
    def __init__(self, slot: int):
        super().__init__(name="ConjureMinorElementals", slot=slot, concentration=True)
        self.dice = (2 * (slot - 3)) * [8]

    def cast(self, character: Character, target: sim.target.Target | None = None):
        super().cast(character, target)
        character.events.add(self, "attack_result")

    def attack_result(self, args: "sim.events.AttackResultArgs"):
        if args.hits():
            args.add_damage(source=self.name, dice=self.dice)

    def end(self, character: Character):
        character.events.remove(self)

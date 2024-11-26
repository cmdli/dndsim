import sim.target
import sim.character
from sim.target import Target
import sim.events


class Spell:
    def __init__(
        self, name: str, slot: int, concentration: bool = False, duration: int = 0
    ):
        self.name = name
        self.slot = slot
        self.concentration = concentration
        self.character: "sim.character.Character" = None
        self.duration = duration
        self.tags = set()

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        self.character = character

    def end(self, character: "sim.character.Character"):
        self.character = None

    def add_tag(self, tag: str):
        self.tags.add(tag)

    def has_tag(self, tag: str):
        return tag in self.tags


class ConcentrationSpell(Spell):
    def __init__(self, name: str, slot: int, **kwargs):
        super().__init__(name, slot, concentration=True, **kwargs)

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        super().cast(character, target)
        character.add_effect(self.name)

    def end(self, character: "sim.character.Character"):
        super().end(character)
        character.remove_effect(self.name)


class BasicSaveSpell(Spell):
    def cast(self, character: "sim.character.Character", target: Target):
        super().cast(character, target)
        dmg = self.damage()
        if target.save(character.spells.dc()):
            dmg = dmg // 2
        target.damage_source(self.name, dmg)

    def damage(self):
        return 0

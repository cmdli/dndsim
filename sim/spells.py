import sim.target
import sim.character
from sim.target import Target
import sim.events
from typing import List, Optional
import util.taggable


class Spell(util.taggable.Taggable):
    def __init__(
        self, name: str, slot: int, concentration: bool = False, duration: int = 0
    ):
        self.name = name
        self.slot = slot
        self.concentration = concentration
        self.duration = duration

    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        self.character = character

    def end(self, character: "sim.character.Character"):
        pass


class TargetedSpell(Spell):
    def cast(self, character: "sim.character.Character", target: Target | None = None):
        super().cast(character, target)
        if not target:
            return
        self.cast_target(character, target)

    def cast_target(self, character: "sim.character.Character", target: Target):
        pass


class ConcentrationSpell(Spell):
    def __init__(self, name: str, slot: int, **kwargs):
        super().__init__(name, slot, concentration=True, **kwargs)

    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        super().cast(character, target)
        character.add_effect(self.name)

    def end(self, character: "sim.character.Character"):
        super().end(character)
        character.remove_effect(self.name)


class BasicSaveSpell(Spell):
    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        if not target:
            return
        super().cast(character, target)
        saved = target.save(character.spells.dc())
        character.do_damage(
            target,
            self.name,
            dice=self.dice(),
            flat_dmg=self.flat_damage(),
            spell=self,
            multiplier=0.5 if saved else 1,
        )

    def dice(self) -> List[int]:
        return []

    def flat_damage(self) -> int:
        return 0

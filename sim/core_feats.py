from typing import Optional

import sim.feat
import sim.spells


class ClassLevels(sim.feat.Feat):
    def __init__(
        self,
        name: str,
        level: int,
        spellcaster: Optional["sim.spells.Spellcaster"] = None,
    ):
        self.class_name = name
        self.level = level
        self.spellcaster = spellcaster

    def apply(self, character):
        super().apply(character)
        if self.spellcaster is not None:
            character.spells.add_spellcaster_level(self.spellcaster, self.level)


class Vex(sim.feat.Feat):
    def __init__(self) -> None:
        self.vexing = False

    def short_rest(self):
        self.vexing = False

    def attack_roll(self, args):
        if self.vexing:
            args.adv = True
            self.vexing = False

    def attack_result(self, args):
        weapon = args.attack.weapon
        if (
            args.hits()
            and weapon
            and weapon.mastery == "Vex"
            and "Vex" in self.character.masteries
        ):
            self.vexing = True


class Topple(sim.feat.Feat):
    def attack_result(self, args):
        weapon = args.attack.weapon
        if not weapon or args.misses():
            return
        target = args.attack.target
        if weapon.mastery == "Topple" and "Topple" in self.character.masteries:
            mod = weapon.mod(self.character)
            if not target.save(self.character.dc(mod)):
                target.knock_prone()


class Graze(sim.feat.Feat):
    def attack_result(self, args):
        weapon = args.attack.weapon
        if not weapon or not args.misses():
            return
        if weapon.mastery == "Graze" and "Graze" in self.character.masteries:
            mod = weapon.mod(self.character)
            args.attack.target.damage_source("Graze", self.character.mod(mod))

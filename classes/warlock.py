from typing import List, Optional

from feats import ASI
from sim.character import Character
import sim.character
from sim.events import AttackResultArgs
from sim.target import Target
from spells.summons import SummonFey, SummonFiend
from spells.warlock import EldritchBlast
from spells.wizard import Blight, FingerOfDeath, Fireball
from util.util import apply_asi_feats, apply_feats_at_levels

import sim.core_feats
import sim.feat


class WarlockLevel(sim.core_feats.ClassLevels):
    def __init__(self, level):
        super().__init__(name="Warlock", level=level)

    def apply(self, character: Character):
        super().apply(character)
        character.spells.add_pact_spellcaster_level(self.level)


class AgonizingBlast(sim.feat.Feat):
    def attack_result(self, args: AttackResultArgs):
        if (
            args.hits()
            and args.attack.spell is not None
            and args.attack.spell.name == "EldritchBlast"
        ):
            args.add_damage(source="Agonizing Blast", damage=self.character.mod("cha"))


class MysticArcanum(sim.feat.Feat):
    def __init__(self, spell_name: str):
        self.spell_name = spell_name

    def apply(self, character: Character):
        character.add_resource(self.spell_name)
        character.resources[self.spell_name].increase_max(1)


def warlock_feats(
    level: int,
    invocations: Optional[List["sim.feat.Feat"]] = None,
    asis: Optional[List["sim.feat.Feat"]] = None,
    arcanums: Optional[List[str]] = None,
) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 1:
        feats.append(WarlockLevel(level))
    # TODO: Level 2 (Magical Cunning)
    # Level 9 (Contact Patron) is irrelevant
    if level >= 11:
        feats.append(MysticArcanum(arcanums[0]))
    if level >= 13:
        feats.append(MysticArcanum(arcanums[1]))
    if level >= 15:
        feats.append(MysticArcanum(arcanums[2]))
    if level >= 17:
        feats.append(MysticArcanum(arcanums[3]))
    # TODO: Level 20 (Eldritch Master)
    apply_asi_feats(level, feats, asis)
    apply_feats_at_levels(
        level,
        feats,
        schedule=[1, 2, 2, 5, 5, 7, 9, 12, 15, 18],
        new_feats=invocations,
    )
    return feats


def fiend_warlock_feats(level: int) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    # Level 3 (Dark One's Blessing) is irrelevant
    # Level 6 (Dark One's Own Luck) is irrelevant
    # Level 10 (Fiendish Resilience) is irrelevant
    # TODO: Level 14 (Hurl Through Hell)
    return feats


class FiendWarlockAction(sim.feat.Feat):
    def action(self, target: Target):
        if (
            self.character.has_resource("SummonFiend")
            and not self.character.spells.is_concentrating()
        ):
            self.character.resources["SummonFiend"].use()
            self.character.spells.cast(
                SummonFiend(slot=6), target=target, ignore_slot=True
            )
        elif self.character.has_resource("FingerOfDeath"):
            self.character.resources["FingerOfDeath"].use()
            self.character.spells.cast(
                FingerOfDeath(slot=7), target=target, ignore_slot=True
            )
        else:
            slot = self.character.spells.highest_slot()
            if slot >= 4 and not self.character.spells.is_concentrating():
                self.character.spells.cast(SummonFey(slot), target=target)
            elif slot >= 5:
                self.character.spells.cast(Blight(slot), target=target)
            elif slot >= 3:
                self.character.spells.cast(Fireball(slot), target=target)
            else:
                self.character.spells.cast(EldritchBlast(), target=target)


class FiendWarlock(sim.character.Character):
    def __init__(self, level: int):
        super().__init__()
        feats: List["sim.feat.Feat"] = []
        feats.extend(
            warlock_feats(
                level,
                asis=[ASI(["cha"]), ASI(["cha", "dex"])],
                invocations=[AgonizingBlast()],
                arcanums=[
                    "SummonFiend",
                    "FingerOfDeath",
                    "Befuddlement",
                    "PowerWordKill",
                ],
            )
        )
        feats.extend(fiend_warlock_feats(level))
        feats.append(FiendWarlockAction())
        # Mystic Arcanum options
        # * Common resource for Mystic Arcanum spells
        # * Ability to store spells that can be cast
        # * Feat for each Mystic Arcanum spell
        super().init(
            level=level,
            stats=[10, 10, 10, 10, 10, 17],
            base_feats=feats,
            spell_mod="cha",
        )

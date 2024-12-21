from typing import List, Optional

from util.util import get_magic_weapon, apply_asi_feats
from sim.spells import Spellcaster
from feats import ASI
from spells.cleric import SpiritGuardians, TollTheDead, InflictWounds, GuardianOfFaith
from spells.summons import SummonCelestial
from weapons import Warhammer

import sim.core_feats
import sim.weapons
import sim.spells
import sim.character
import sim.target
import sim.feat


class ClericLevel(sim.core_feats.ClassLevels):
    def __init__(self, level: int):
        super().__init__(name="Cleric", level=level, spellcaster=Spellcaster.FULL)


class ClericAction(sim.feat.Feat):
    def action(self, target: "sim.target.Target"):
        slot = self.character.spells.highest_slot()
        spell: Optional["sim.spells.Spell"] = None
        if not self.character.spells.is_concentrating() and slot >= 3:
            if slot >= 5:
                spell = SummonCelestial(slot)
            elif slot >= 3:
                spell = SpiritGuardians(slot)
        else:
            slot = self.character.spells.highest_slot(max=4)
            if slot >= 4:
                spell = GuardianOfFaith(slot)
            elif slot >= 1:
                spell = InflictWounds(slot)
            else:
                spell = TollTheDead()
        if spell is not None:
            self.character.spells.cast(spell, target)


class WarPriest(sim.feat.Feat):
    def __init__(self, weapon: "sim.weapons.Weapon") -> None:
        self.weapon = weapon

    def short_rest(self):
        self.uses = self.character.mod("wis")

    def after_action(self, target: sim.target.Target):
        if self.uses > 0 and self.character.use_bonus("WarPriest"):
            self.character.weapon_attack(target, self.weapon)


class BlessedStrikes(sim.feat.Feat):
    def __init__(self, num_dice: int) -> None:
        self.num_dice = num_dice

    def begin_turn(self, target):
        self.used = False

    def attack_result(self, args):
        if args.hits() and not self.used:
            self.used = True
            args.add_damage("BlessedStrikes", dice=self.num_dice * [8])


def cleric_feats(
    level: int, asis: Optional[List["sim.feat.Feat"]] = None
) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 1:
        feats.append(ClericLevel(level))
    # Level 1 (Divine Order) is irrelevant
    # TODO: Level 2 (Channel Divinity)
    # Level 5 (Sear Undead) is irrelevant
    if level >= 7:
        feats.append(BlessedStrikes(2 if level >= 14 else 1))
    # TODO: Level 7 (Blessed Strikes) for Potent Spellcasting
    # TODO: Level 10 (Divine Intervention)
    # TODO: Level 20 (Divine Intervention)
    apply_asi_feats(level=level, feats=feats, asis=asis)
    return feats


def war_cleric_feats(level: int, weapon: "sim.weapons.Weapon") -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    # TODO: Level 3 (Guided Strike)
    if level >= 3:
        feats.append(WarPriest(weapon))
    # TODO: Level 6 (War God's Blessing)
    # Level 17 (Avatar of Battle) is irrelevant
    return feats


class Cleric(sim.character.Character):
    def __init__(self, level: int) -> None:
        magic_weapon = get_magic_weapon(level)
        weapon = Warhammer(magic_bonus=magic_weapon)
        feats: List["sim.feat.Feat"] = []
        # TODO: Add Origin Feat
        # TODO: Add Epic Boon
        feats.extend(
            cleric_feats(
                level,
                asis=[ASI(["wis"]), ASI(["wis", "str"]), ASI(["str"]), ASI(["str"])],
            )
        )
        feats.extend(war_cleric_feats(level, weapon))
        feats.append(ClericAction())
        super().init(
            level=level,
            stats=[15, 10, 10, 10, 17, 10],
            base_feats=feats,
            spell_mod="wis",
        )

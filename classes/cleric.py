from typing import List, Optional

from util.util import (
    get_magic_weapon,
)
from sim.spells import Spellcaster
from feats import ASI
from spells.cleric import SpiritGuardians, TollTheDead, InflictWounds, GuardianOfFaith
from spells.summons import SummonCelestial
from weapons import Warhammer

import sim.weapons
import sim.spells
import sim.character
import sim.target
import sim.feat


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


class Cleric(sim.character.Character):
    def __init__(self, level: int) -> None:
        magic_weapon = get_magic_weapon(level)
        weapon = Warhammer(magic_bonus=magic_weapon)
        base_feats: List["sim.feat.Feat"] = []
        base_feats.append(ClericAction())
        if level >= 3:
            base_feats.append(WarPriest(weapon))
        if level >= 4:
            base_feats.append(ASI(["wis"]))
        if level >= 7:
            base_feats.append(BlessedStrikes(2 if level >= 14 else 1))
        if level >= 8:
            base_feats.append(ASI(["wis", "str"]))
        if level >= 12:
            base_feats.append(ASI(["str"]))
        if level >= 16:
            base_feats.append(ASI(["str"]))
        super().init(
            level=level,
            stats=[15, 10, 10, 10, 17, 10],
            base_feats=base_feats,
            spellcaster=Spellcaster.FULL,
            spell_mod="wis",
        )

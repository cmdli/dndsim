import random
from util.util import (
    prof_bonus,
    get_magic_weapon,
    cantrip_dice,
    highest_spell_slot,
    spell_slots,
    roll_dice,
    do_roll,
)
import sim.character
from sim.spellcasting import Spellcaster
from sim.feat import Feat
from sim.feats import ASI
from spells.cleric import SpiritGuardians, TollTheDead, InflictWounds, GuardianOfFaith
from sim.summons import SummonCelestial
from sim.weapons import Weapon, Warhammer


class ClericAction(Feat):
    def action(self, target: sim.character.Target):
        slot = self.character.spells.highest_slot()
        spell = None
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


class WarPriest(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.weapon = weapon

    def short_rest(self):
        self.uses = self.character.mod("wis")

    def after_action(self, target: sim.character.Target):
        if self.uses > 0 and self.character.use_bonus("WarPriest"):
            self.character.attack(target, self.weapon)


class BlessedStrikes(Feat):
    def __init__(self, num_dice: int) -> None:
        self.num_dice = num_dice

    def begin_turn(self, target: sim.character.Target):
        self.used = False

    def hit(self, args: sim.character.HitArgs):
        if not self.used:
            self.used = True
            args.add_damage("BlessedStrikes", roll_dice(self.num_dice, 8))


class Cleric(sim.character.Character):
    def __init__(self, level: int) -> None:
        magic_weapon = get_magic_weapon(level)
        weapon = Warhammer(magic_bonus=magic_weapon)
        base_feats = []
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

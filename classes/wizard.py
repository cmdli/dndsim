from typing import List, Optional

from util.util import (
    apply_asi_feats,
    get_magic_weapon,
    safe_cast,
)
from sim.spells import Spellcaster
from spells.wizard import (
    MeteorSwarm,
    Fireball,
    Firebolt,
    MagicMissile,
    FingerOfDeath,
    Blight,
    ChainLightning,
    ScorchingRay,
)
from feats import ASI
from sim.spells import Spell, School
from spells.summons import SummonFey

import sim.attack
import sim.feat
import sim.character
import sim.target


class WizardLevel(sim.core_feats.ClassLevels):
    def __init__(self, level: int):
        super().__init__(name="Wizard", level=level, spellcaster=Spellcaster.FULL)


class WandOfTheWarMage(sim.feat.Feat):
    def __init__(self, bonus: int) -> None:
        super().__init__()
        self.bonus = bonus

    def apply(self, character: sim.character.Character):
        super().apply(character)
        character.spells.to_hit_bonus += self.bonus


class PotentCantrip(sim.feat.Feat):
    # TODO: Add damage when enemy saves against a cantrip
    def attack_result(self, args):
        if args.hits():
            return
        attack = safe_cast(sim.attack.SpellAttack, args.attack.attack)
        if attack and attack.spell.slot == 0:
            spell = attack.spell
            self.character.do_damage(
                target=args.attack.target,
                damage=sim.attack.DamageRoll(
                    source="PotentCantrip", dice=attack.damage.dice
                ),
                spell=spell,
                multiplier=0.5,
            )


class EmpoweredEvocation(sim.feat.Feat):
    def damage_roll(self, args):
        if (
            args.spell
            and not args.spell.has_tag("EmpoweredEvocationUsed")
            and args.spell.school is School.Evocation
        ):
            args.spell.add_tag("EmpoweredEvocationUsed")
            args.damage.flat_dmg += self.character.mod("int")


class Overchannel(sim.feat.Feat):
    def __init__(self) -> None:
        self.used = False

    def long_rest(self):
        # Only use once per long rest
        self.used = False

    def damage_roll(self, args):
        if (
            args.spell
            and args.spell.slot >= 3
            and args.spell.slot <= 5
            and not self.used
        ):
            self.used = True
            for i in range(len(args.damage.rolls)):
                args.damage.rolls[i] = args.damage.dice[i]


def wizard_feats(
    level: int, asis: Optional[List["sim.feat.Feat"]] = None
) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 1:
        feats.append(WizardLevel(level))
    # Level 1 (Ritual Adept) is irrelevant
    # TODO: Level 1 (Arcane Recovery)
    # Level 5 (Memorize Spell) is irrelevant
    # TODO: Level 18 (Spell Mastery)
    # TODO: Level 20 (Signature Spells)
    apply_asi_feats(level, feats, asis)
    return feats


def evocation_wizard_feats(level: int) -> List["sim.feat.Feat"]:
    feats: List["sim.feat.Feat"] = []
    if level >= 3:
        feats.append(PotentCantrip())
    # Level 6 (Sculpt Spells) is irrelevant
    if level >= 10:
        feats.append(EmpoweredEvocation())
    if level >= 14:
        feats.append(Overchannel())
    return feats


class WizardAction(sim.feat.Feat):
    def action(self, target: "sim.target.Target"):
        slot = self.character.spells.highest_slot()
        spell: Optional[Spell] = None
        if slot >= 3 and not self.character.spells.is_concentrating():
            spell = SummonFey(slot)
        elif slot >= 9:
            spell = MeteorSwarm(slot)
        elif slot >= 7:
            spell = FingerOfDeath(slot)
        elif slot >= 6:
            spell = ChainLightning(slot)
        elif slot >= 4:
            spell = Blight(slot)
        elif slot >= 3:
            spell = Fireball(slot)
        elif slot >= 2 and self.character.level < 11:
            spell = ScorchingRay(slot)
        elif slot >= 1 and self.character.level < 5:
            spell = MagicMissile(slot)
        else:
            spell = Firebolt()
        if spell is not None:
            self.character.spells.cast(spell, target)


class EvocationWizard(sim.character.Character):
    def __init__(self, level: int) -> None:
        magic_weapon = get_magic_weapon(level)
        feats: List["sim.feat.Feat"] = []
        feats.append(WizardAction())
        feats.append(WandOfTheWarMage(magic_weapon))
        feats.extend(
            wizard_feats(
                level,
                asis=[
                    ASI(["int"]),
                    ASI(["int", "wis"]),
                    ASI(),
                    ASI(),
                    ASI(),
                ],
            )
        )
        feats.extend(evocation_wizard_feats(level))
        super().init(
            level=level,
            stats=[10, 10, 10, 17, 10, 10],
            base_feats=feats,
            spell_mod="int",
        )

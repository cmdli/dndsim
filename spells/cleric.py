from typing import List, override, Optional

from util.util import roll_dice, cantrip_dice
from sim.target import Target
import sim.event_loop
import sim.spells
import sim.weapons
import sim.character


class SpiritGuardians(sim.spells.ConcentrationSpell, sim.event_loop.Listener):
    def __init__(self, slot: int, **kwargs):
        super().__init__("SpiritGuardians", slot=slot, **kwargs)

    def cast(
        self, character: "sim.character.Character", target: Optional[Target] = None
    ):
        super().cast(character, target)
        character.events.add(self, ["enemy_turn"])

    def end(self, character: "sim.character.Character"):
        character.events.remove(self)

    def enemy_turn(self, target: Target):
        dmg = roll_dice(self.slot, 8)
        if target.save(self.character.spells.dc()):
            dmg = dmg // 2
        target.damage_source("SpiritGuardians", dmg)


class TollTheDead(sim.spells.TargetedSpell):
    def __init__(self):
        super().__init__("TollTheDead", slot=0, concentration=False)

    def cast_target(self, character: "sim.character.Character", target: Target):
        num_dice = cantrip_dice(character.level)
        if not target.save(character.spells.dc()):
            if target.dmg > 0:
                dmg = roll_dice(num_dice, 12)
            else:
                dmg = roll_dice(num_dice, 8)
            target.damage_source("TollTheDead", dmg)


class Harm(sim.spells.BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("Harm", slot=slot, dice=14 * [6])
        assert slot >= 6


class InflictWounds(sim.spells.BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("InflictWounds", slot, dice=(1 + self.slot) * [10])


class SpiritualWeaponWeapon(sim.weapons.Weapon):
    def __init__(self, slot: int, **kwargs):
        super().__init__(
            name="SpiritualWeaponWeapon",
            num_dice=slot - 1,
            die=8,
            damage_type="force",
            override_mod="wis",
        )

    def to_hit(self, character: "sim.character.Character"):
        return character.prof + character.mod("wis")


class SpiritualWeapon(sim.spells.Spell, sim.event_loop.Listener):
    def __init__(self, slot: int, concentration: bool = True):
        super().__init__("SpiritualWeapon", slot=slot, concentration=concentration)
        self.weapon = SpiritualWeaponWeapon(slot=self.slot)

    def cast(
        self, character: "sim.character.Character", target: Optional[Target] = None
    ):
        super().cast(character, target)
        character.events.add(self, ["after_action"])

    def end(self, character: "sim.character.Character"):
        super().end(character)
        character.events.remove(self)

    def after_action(self, target: Target):
        if self.character.use_bonus("SpiritualWeapon"):
            self.character.weapon_attack(target, self.weapon)


class GuardianOfFaith(sim.spells.Spell, sim.event_loop.Listener):
    def __init__(self, slot: int):
        super().__init__("GuardianOfFaith", slot, duration=10)
        self.dmg = 60

    def cast(
        self, character: "sim.character.Character", target: Optional[Target] = None
    ):
        super().cast(character, target)
        character.events.add(self, ["enemy_turn"])

    def end(self, character: "sim.character.Character"):
        super().end(character)
        character.events.remove(self)

    def enemy_turn(self, target: Target):
        if not target.save(self.character.spells.dc()):
            target.damage_source("GuardianOfFaith", 20)
            self.dmg -= 20
            if self.dmg <= 0:
                self.character.spells.end_spell(self)

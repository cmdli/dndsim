from typing import List, override, Optional
from sim.events import AttackResultArgs
from sim.spells import ConcentrationSpell, Spell, BasicSaveSpell
from util.util import roll_dice, cantrip_dice
from sim.character import Character
from sim.target import Target
from sim.weapons import Weapon
import sim.event_loop


class SpiritGuardians(ConcentrationSpell, sim.event_loop.Listener):
    def __init__(self, slot: int, **kwargs):
        super().__init__("SpiritGuardians", slot=slot, **kwargs)

    def cast(self, character: Character, target: Optional[Target] = None):
        super().cast(character, target)
        character.events.add(self, ["enemy_turn"])

    def end(self, character: Character):
        character.events.remove(self)

    def enemy_turn(self, target: Target):
        dmg = roll_dice(self.slot, 8)
        if target.save(self.character.spells.dc()):
            dmg = dmg // 2
        target.damage_source("SpiritGuardians", dmg)


class TollTheDead(Spell):
    def __init__(self):
        super().__init__("TollTheDead", slot=0, concentration=False)

    def cast(self, character: Character, target: Optional[Target] = None):
        super().cast(character, target)
        if not target:
            return
        num_dice = cantrip_dice(character.level)
        if not target.save(character.spells.dc()):
            if target.dmg > 0:
                dmg = roll_dice(num_dice, 12)
            else:
                dmg = roll_dice(num_dice, 8)
            target.damage_source("TollTheDead", dmg)


class Harm(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("Harm", slot=slot)
        assert slot >= 6

    def dice(self) -> List[int]:
        return 14 * [6]


class InflictWounds(BasicSaveSpell):
    def __init__(self, slot: int):
        super().__init__("InflictWounds", slot)

    def dice(self) -> List[int]:
        num_dice = 1 + self.slot
        return num_dice * [10]


class SpiritualWeaponWeapon(Weapon):
    def __init__(self, slot: int, **kwargs):
        super().__init__(
            name="SpiritualWeaponWeapon",
            num_dice=slot - 1,
            die=8,
            damage_type="force",
            override_mod="wis",
        )

    def to_hit(self, character: Character):
        return character.prof + character.mod("wis")


class SpiritualWeapon(Spell, sim.event_loop.Listener):
    def __init__(self, slot: int, concentration: bool = True):
        super().__init__("SpiritualWeapon", slot=slot, concentration=concentration)
        self.weapon = SpiritualWeaponWeapon(slot=self.slot)

    def cast(self, character: Character, target: Optional[Target] = None):
        super().cast(character, target)
        character.events.add(self, ["after_action"])

    def end(self, character: Character):
        super().end(character)
        character.events.remove(self)

    def after_action(self, target: Target):
        if self.character.use_bonus("SpiritualWeapon"):
            self.character.weapon_attack(target, self.weapon)


class GuardianOfFaith(Spell, sim.event_loop.Listener):
    def __init__(self, slot: int):
        super().__init__("GuardianOfFaith", slot, duration=10)
        self.dmg = 60

    def cast(self, character: Character, target: Optional[Target] = None):
        super().cast(character, target)
        character.events.add(self, ["enemy_turn"])

    def end(self, character: Character):
        super().end(character)
        character.events.remove(self)

    def enemy_turn(self, target: Target):
        if not target.save(self.character.spells.dc()):
            target.damage_source("GuardianOfFaith", 20)
            self.dmg -= 20
            if self.dmg <= 0:
                self.character.spells.end_spell(self)

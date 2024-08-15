import sim.target
from util.util import roll_dice, cantrip_dice
from sim.weapons import Weapon
import sim.character
from sim.target import Target
from sim.events import HitArgs
from util.log import log


class Spell:
    def __init__(
        self, name: str, slot: int, concentration: bool = False, duration: int = 0
    ):
        self.name = name
        self.slot = slot
        self.concentration = concentration
        self.character: "sim.character.Character" = None
        self.duration = duration

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        self.character = character

    def end(self, character: "sim.character.Character"):
        self.character = None


class ConcentrationSpell(Spell):
    def __init__(self, name: str, slot: int, **kwargs):
        super().__init__(name, slot, concentration=True, **kwargs)

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        super().cast(character, target)
        character.add_effect(self.name)

    def end(self, character: "sim.character.Character"):
        super().end(character)
        character.remove_effect(self.name)


class HuntersMark(ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("HuntersMark", slot)


class DivineSmite(Spell):
    def __init__(self, slot: int, crit: bool):
        super().__init__("DivineSmite", slot=slot)
        self.crit = crit

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        num_dice = 1 + self.slot
        if self.crit:
            num_dice *= 2
        target.damage_source("DivineSmite", roll_dice(num_dice, 8))


class DivineFavor(ConcentrationSpell):
    def __init__(self, slot: int):
        super().__init__("DivineFavor", slot)


class Fireball(Spell):
    def __init__(self, slot: int):
        super().__init__("Fireball", slot)

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        dmg = roll_dice(5 + self.slot, 6)
        if target.save(character.spells.dc()):
            dmg = dmg // 2
        target.damage_source("Fireball", dmg)


class TrueStrike(Spell):
    def __init__(self, weapon: Weapon, **kwargs):
        super().__init__("TrueStrike", 0)
        self.weapon = weapon

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        character.attack(target, self.weapon, tags=["truestrike"])


class HolyWeapon(ConcentrationSpell):
    def __init__(self, slot: int, **kwargs):
        super().__init__("HolyWeapon", slot=slot, **kwargs)


class EldritchBlastBolt(Weapon):
    def __init__(self, **kwargs):
        super().__init__("EldritchBlastBolt", num_dice=1, die=10, mod="none")


class EldritchBlast(Spell):
    def __init__(self, character_level: int, **kwargs):
        super().__init__("EldritchBlast", 0, **kwargs)
        self.character_level = character_level
        self.weapon = EldritchBlastBolt()
        self.num_bolts = cantrip_dice(character_level)

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        for _ in range(self.num_bolts):
            character.attack(target, self.weapon)


class SpiritGuardians(ConcentrationSpell):
    def __init__(self, slot: int, **kwargs):
        super().__init__("SpiritGuardians", slot=slot, **kwargs)

    def cast(self, character: "sim.character.Character", target: "sim.target.Target"):
        super().cast(character, target)
        character.events.add(self, "enemy_turn")

    def end(self, character: "sim.character.Character"):
        character.events.remove(self)

    def enemy_turn(self, target: Target):
        dmg = roll_dice(self.slot, 8)
        if target.save(self.character.spells.dc()):
            dmg = dmg // 2
        target.damage_source("SpiritGuardians", dmg // 2)


class TollTheDead(Spell):
    def __init__(self):
        super().__init__("TollTheDead", slot=0, concentration=False)

    def cast(self, character: "sim.character.Character", target: Target):
        super().cast(character, target)
        num_dice = cantrip_dice(character.level)
        if not target.save(character.spells.dc()):
            if target.dmg > 0:
                dmg = roll_dice(num_dice, 12)
            else:
                dmg = roll_dice(num_dice, 8)
            target.damage_source("TollTheDead", dmg)


class Harm(Spell):
    def __init__(self, slot: int):
        super().__init__("Harm", slot=slot)

    def cast(self, character: "sim.character.Character", target: Target):
        super().cast(character, target)
        dmg = roll_dice(14, 6)
        if target.save(character.spells.dc()):
            dmg = dmg // 2
        target.damage_source("Harm", dmg)


class InflictWounds(Spell):
    def __init__(self, slot: int):
        super().__init__("InflictWounds", slot)

    def cast(self, character: "sim.character.Character", target: Target):
        super().cast(character, target)
        num_dice = 1 + self.slot
        dmg = roll_dice(num_dice, 10)
        if target.save(character.spells.dc()):
            dmg = dmg // 2
        target.damage_source("InflictWounds", dmg)


class SpiritualWeaponWeapon(Weapon):
    def __init__(self, slot: int, **kwargs):
        super().__init__(
            name="SpiritualWeaponWeapon", num_dice=slot - 1, die=8, damage_type="force"
        )

    def to_hit(self, character: "sim.character.Character"):
        return character.prof + character.mod("wis")

    def damage(self, character: "sim.character.Character", args: HitArgs):
        return character.weapon_roll(self, crit=args.crit) + character.mod(
            character.spells.mod
        )


class SpiritualWeapon(Spell):
    def __init__(self, slot: int, concentration: bool = True):
        super().__init__("SpiritualWeapon", slot=slot, concentration=concentration)
        self.weapon = SpiritualWeaponWeapon(slot=self.slot)

    def cast(self, character: "sim.character.Character", target: Target):
        super().cast(character, target)
        character.events.add(self, ["after_action"])

    def end(self, character: "sim.character.Character"):
        super().end(character)
        character.events.remove(self)

    def after_action(self, target: Target):
        if self.character.use_bonus("SpiritualWeapon"):
            self.character.attack(target, self.weapon)


class GuardianOfFaith(Spell):
    def __init__(self, slot: int):
        super().__init__("GuardianOfFaith", slot, duration=10)
        self.dmg = 60

    def cast(self, character: "sim.character.Character", target: Target):
        super().cast(character, target)
        character.events.add(self, "enemy_turn")

    def end(self, character: "sim.character.Character"):
        super().end(character)
        character.events.remove(self)

    def enemy_turn(self, target: Target):
        if not target.save(self.character.spells.dc()):
            target.damage_source("GuardianOfFaith", 20)
            self.dmg -= 20
            if self.dmg <= 0:
                self.character.spells.end_spell(self)

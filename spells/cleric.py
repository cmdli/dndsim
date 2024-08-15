from sim.spells import ConcentrationSpell, Spell
from util.util import roll_dice, cantrip_dice
from sim.character import Character
from sim.target import Target
from sim.events import HitArgs
from sim.weapons import Weapon


class SpiritGuardians(ConcentrationSpell):
    def __init__(self, slot: int, **kwargs):
        super().__init__("SpiritGuardians", slot=slot, **kwargs)

    def cast(self, character: Character, target: Target):
        super().cast(character, target)
        character.events.add(self, "enemy_turn")

    def end(self, character: Character):
        character.events.remove(self)

    def enemy_turn(self, target: Target):
        dmg = roll_dice(self.slot, 8)
        if target.save(self.character.spells.dc()):
            dmg = dmg // 2
        target.damage_source("SpiritGuardians", dmg // 2)


class TollTheDead(Spell):
    def __init__(self):
        super().__init__("TollTheDead", slot=0, concentration=False)

    def cast(self, character: Character, target: Target):
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

    def cast(self, character: Character, target: Target):
        super().cast(character, target)
        dmg = roll_dice(14, 6)
        if target.save(character.spells.dc()):
            dmg = dmg // 2
        target.damage_source("Harm", dmg)


class InflictWounds(Spell):
    def __init__(self, slot: int):
        super().__init__("InflictWounds", slot)

    def cast(self, character: Character, target: Target):
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

    def to_hit(self, character: Character):
        return character.prof + character.mod("wis")

    def damage(self, character: Character, args: HitArgs):
        return character.weapon_roll(self, crit=args.crit) + character.mod(
            character.spells.mod
        )


class SpiritualWeapon(Spell):
    def __init__(self, slot: int, concentration: bool = True):
        super().__init__("SpiritualWeapon", slot=slot, concentration=concentration)
        self.weapon = SpiritualWeaponWeapon(slot=self.slot)

    def cast(self, character: Character, target: Target):
        super().cast(character, target)
        character.events.add(self, ["after_action"])

    def end(self, character: Character):
        super().end(character)
        character.events.remove(self)

    def after_action(self, target: Target):
        if self.character.use_bonus("SpiritualWeapon"):
            self.character.attack(target, self.weapon)


class GuardianOfFaith(Spell):
    def __init__(self, slot: int):
        super().__init__("GuardianOfFaith", slot, duration=10)
        self.dmg = 60

    def cast(self, character: Character, target: Target):
        super().cast(character, target)
        character.events.add(self, "enemy_turn")

    def end(self, character: Character):
        super().end(character)
        character.events.remove(self)

    def enemy_turn(self, target: Target):
        if not target.save(self.character.spells.dc()):
            target.damage_source("GuardianOfFaith", 20)
            self.dmg -= 20
            if self.dmg <= 0:
                self.character.spells.end_spell(self)

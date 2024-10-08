from typing import List
from sim.events import AttackRollArgs, HitArgs
from sim.feats import Feat
from sim.target import Target
from sim.character import Character
from sim.weapons import Weapon
from sim.spells import Spell


class SummonAction(Feat):
    def __init__(self, slot: int, weapon: Weapon) -> None:
        self.slot = slot
        self.weapon = weapon

    def action(self, target: Target):
        for _ in range(self.slot // 2):
            self.character.attack(target, self.weapon)


class SummonWeapon(Weapon):
    def __init__(self, caster: Character = None, **kwargs):
        super().__init__(**kwargs)
        self.caster = caster

    def to_hit(self, character: Character):
        return self.caster.prof + self.caster.mod(self.caster.spells.mod)

    def damage(self, character: Character, args: HitArgs):
        return character.weapon_roll(self, crit=args.crit) + self.dmg_bonus


class Summon(Character):
    def __init__(self, slot: int, weapon: Weapon, feats=[], **kwargs):
        base_feats = []
        base_feats.append(SummonAction(slot, weapon))
        base_feats.extend(feats)
        super().init(
            level=1,
            stats=[10, 10, 10, 10, 10, 10],
            base_feats=base_feats,
        )


class SummonSpell(Spell):
    def __init__(self, name: str, slot: int):
        super().__init__(name, slot, concentration=True)
        self.character = None

    def summon(self, caster: Character):
        return None

    def cast(self, character: Character, target: Target):
        self.minion = self.summon(character)
        character.add_minion(self.minion)
        self.character = character

    def end(self, character: Character):
        if self.character is not None:
            self.character.remove_minion(self.minion)


class FeyWeapon(SummonWeapon):
    def __init__(self, slot: int, **kwargs):
        super().__init__(
            name="FeyWeapon", num_dice=2, die=6, dmg_bonus=3 + slot, **kwargs
        )


class Mirthful(Feat):
    def begin_turn(self, target: Target):
        self.used = False

    def roll_attack(self, args: AttackRollArgs):
        if not self.used:
            args.adv = True
            self.used = True


class FeySummon(Summon):
    def __init__(self, slot: int, caster: Character):
        super().__init__(
            slot=slot,
            weapon=FeyWeapon(slot, caster=caster),
            feats=[Mirthful()],
        )


class SummonFey(SummonSpell):
    def __init__(self, slot: int):
        super().__init__(
            "SummonFey",
            slot,
        )

    def summon(self, caster: Character):
        return FeySummon(self.slot, caster)


class CelestialWeapon(SummonWeapon):
    def __init__(self, slot: int, **kwargs):
        super().__init__(
            name="CelestialWeapon", num_dice=2, die=6, dmg_bonus=2 + slot, **kwargs
        )


class CelestialSummon(Summon):
    def __init__(self, slot: int, caster: Character):
        super().__init__(
            slot=slot, weapon=CelestialWeapon(slot=slot, caster=caster), feats=[]
        )


class SummonCelestial(SummonSpell):
    def __init__(self, slot: int):
        super().__init__("SummonCelestial", slot)

    def summon(self, caster: Character):
        return CelestialSummon(self.slot, caster)

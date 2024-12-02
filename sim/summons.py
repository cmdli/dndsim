from typing import override, Optional, List
from sim.events import AttackResultArgs, AttackRollArgs
from sim.feat import Feat
from sim.target import Target
from sim.character import Character
from sim.weapons import Weapon
from sim.spells import Spell


class SummonAction(Feat):
    def __init__(self, slot: int, weapon: Weapon) -> None:
        self.slot = slot
        self.weapon = weapon

    @override
    def action(self, target: Target):
        for _ in range(self.slot // 2):
            self.character.weapon_attack(target, self.weapon)


class SummonWeapon(Weapon):
    def __init__(self, caster: Optional[Character] = None, **kwargs):
        super().__init__(**kwargs)
        self.caster = caster

    @override
    def to_hit(self, character):
        return self.caster.prof + self.caster.mod(self.caster.spells.mod)

    def attack_result(self, args: AttackResultArgs, character: Character):
        num_dice = self.num_dice
        if args.crit:
            num_dice *= 2
        args.add_damage(self.name(), num_dice * [self.die], self.dmg_bonus)


class Summon(Character):
    def __init__(
        self, slot: int, weapon: Weapon, feats: Optional[List[Feat]] = None, **kwargs
    ):
        feats = feats or []
        base_feats: List[Feat] = []
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

    def summon(self, caster: Character):
        return None

    @override
    def cast(self, character: Character, target: Optional[Target] = None):
        self.minion = self.summon(character)
        character.add_minion(self.minion)

    @override
    def end(self, character: Character):
        character.remove_minion(self.minion)


class FeyWeapon(SummonWeapon):
    def __init__(self, slot: int, **kwargs):
        super().__init__(
            name="FeyWeapon", num_dice=2, die=6, dmg_bonus=3 + slot, **kwargs
        )


class Mirthful(Feat):
    def begin_turn(self, target: Target):
        self.used = False

    def attack_roll(self, args: AttackRollArgs):
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

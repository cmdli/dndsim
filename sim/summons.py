from typing import override, Optional, List

from sim.events import AttackResultArgs, AttackRollArgs
from sim.spells import Spell
from util.log import log

import sim.feat
import sim.target
import sim.character
import sim.weapons


class SummonAction(sim.feat.Feat):
    def __init__(self, slot: int, weapon: "sim.weapons.Weapon") -> None:
        self.slot = slot
        self.weapon = weapon

    @override
    def action(self, target: "sim.target.Target"):
        for _ in range(self.slot // 2):
            self.character.weapon_attack(target, self.weapon)


class SummonWeapon(sim.weapons.Weapon):
    def __init__(self, caster: Optional["sim.character.Character"] = None, **kwargs):
        super().__init__(**kwargs)
        self.caster = caster

    @override
    def to_hit(self, character):
        return self.caster.spells.to_hit()

    def attack_result(
        self, args: AttackResultArgs, character: "sim.character.Character"
    ):
        if args.misses():
            return
        num_dice = self.num_dice
        if args.crit:
            num_dice *= 2
        args.add_damage(self.name(), num_dice * [self.die], self.dmg_bonus)


class Summon(sim.character.Character):
    def __init__(
        self,
        slot: int,
        weapon: "sim.weapons.Weapon",
        feats: Optional[List["sim.feat.Feat"]] = None,
        **kwargs
    ):
        feats = feats or []
        base_feats: List["sim.feat.Feat"] = []
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

    def summon(self, caster: "sim.character.Character"):
        return None

    @override
    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        self.minion = self.summon(character)
        character.add_minion(self.minion)

    @override
    def end(self, character: "sim.character.Character"):
        character.remove_minion(self.minion)


class FeyWeapon(SummonWeapon):
    def __init__(self, slot: int, **kwargs):
        super().__init__(
            name="FeyWeapon", num_dice=2, die=6, dmg_bonus=3 + slot, **kwargs
        )


class Mirthful(sim.feat.Feat):
    def __init__(self) -> None:
        super().__init__()
        self.used = False

    def begin_turn(self, target: "sim.target.Target"):
        self.used = False

    def attack_roll(self, args: AttackRollArgs):
        if not self.used:
            log.record("Mirthful", 1)
            args.adv = True
            self.used = True


class FeySummon(Summon):
    def __init__(self, slot: int, caster: "sim.character.Character"):
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

    def summon(self, caster: "sim.character.Character"):
        return FeySummon(self.slot, caster)


class CelestialWeapon(SummonWeapon):
    def __init__(self, slot: int, **kwargs):
        super().__init__(
            name="CelestialWeapon", num_dice=2, die=6, dmg_bonus=2 + slot, **kwargs
        )


class CelestialSummon(Summon):
    def __init__(self, slot: int, caster: "sim.character.Character"):
        super().__init__(
            slot=slot, weapon=CelestialWeapon(slot=slot, caster=caster), feats=[]
        )


class SummonCelestial(SummonSpell):
    def __init__(self, slot: int):
        super().__init__("SummonCelestial", slot)

    def summon(self, caster: "sim.character.Character"):
        return CelestialSummon(self.slot, caster)

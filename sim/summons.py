from typing import override, Optional, List


import sim.spells
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

    def attack_result(self, args, character):
        if args.misses():
            return
        num_dice = self.num_dice
        if args.crit:
            num_dice *= 2
        args.add_damage(self.name, num_dice * [self.die], self.dmg_bonus)


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


class SummonSpell(sim.spells.Spell):
    def __init__(self, name: str, slot: int):
        super().__init__(name, slot, concentration=True)

    def summon(
        self, caster: "sim.character.Character"
    ) -> Optional["sim.character.Character"]:
        return None

    @override
    def cast(
        self,
        character: "sim.character.Character",
        target: Optional["sim.target.Target"] = None,
    ):
        self.minion = self.summon(character)
        if self.minion:
            character.add_minion(self.minion)

    @override
    def end(self, character: "sim.character.Character"):
        if self.minion:
            character.remove_minion(self.minion)

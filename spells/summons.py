import sim.summons
import sim.feat
import sim.character
import sim.target


class FeyWeapon(sim.summons.SummonWeapon):
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

    def attack_roll(self, args):
        if not self.used:
            args.adv = True
            self.used = True


class FeySummon(sim.summons.Summon):
    def __init__(self, slot: int, caster: "sim.character.Character"):
        super().__init__(
            slot=slot,
            weapon=FeyWeapon(slot, caster=caster),
            feats=[Mirthful()],
        )


class SummonFey(sim.summons.SummonSpell):
    def __init__(self, slot: int):
        super().__init__(
            "SummonFey",
            slot,
        )

    def summon(self, caster: "sim.character.Character"):
        return FeySummon(self.slot, caster)


class CelestialWeapon(sim.summons.SummonWeapon):
    def __init__(self, slot: int, **kwargs):
        super().__init__(
            name="CelestialWeapon", num_dice=2, die=6, dmg_bonus=2 + slot, **kwargs
        )


class CelestialSummon(sim.summons.Summon):
    def __init__(self, slot: int, caster: "sim.character.Character"):
        super().__init__(
            slot=slot, weapon=CelestialWeapon(slot=slot, caster=caster), feats=[]
        )


class SummonCelestial(sim.summons.SummonSpell):
    def __init__(self, slot: int):
        super().__init__("SummonCelestial", slot)

    def summon(self, caster: "sim.character.Character"):
        return CelestialSummon(self.slot, caster)


class FiendWeapon(sim.summons.SummonWeapon):
    def __init__(self, slot: int, **kwargs):
        super().__init__(
            name="FiendWeapon", num_dice=2, die=6, dmg_bonus=3 + slot, **kwargs
        )


class FiendSummon(sim.summons.Summon):
    def __init__(self, slot: int, caster: "sim.character.Character"):
        super().__init__(
            slot=slot, weapon=FiendWeapon(slot=slot, caster=caster), feats=[]
        )


class SummonFiend(sim.summons.SummonSpell):
    def __init__(self, slot: int):
        super().__init__("SummonFiend", slot)

    def summon(self, caster: "sim.character.Character"):
        return FiendSummon(self.slot, caster)

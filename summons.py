from events import AttackArgs, AttackRollArgs, HitArgs
from feats import Feat, Attack
from util import do_roll, roll_dice
from target import Target
from log import log
from character import Character
from weapons import Weapon
from spells import Spell


class SummonHit(Feat):
    def __init__(self, slot: int, bonus_dmg: int) -> None:
        self.name = "SummonHit"
        self.bonus_dmg = bonus_dmg
        self.slot = slot

    def hit(self, args: HitArgs):
        num = args.attack.weapon.num_dice
        if args.crit:
            num *= 2
        args.attack.target.damage_source(
            self.name,
            roll_dice(num, args.attack.weapon.die) + self.bonus_dmg + self.slot,
        )


class SummonAction(Feat):
    def __init__(self, slot: int, weapon: Weapon) -> None:
        self.name = "SummonAction"
        self.slot = slot
        self.weapon = weapon

    def action(self, target: Target):
        for _ in range(self.slot // 2):
            self.character.attack(target, self.weapon)


class Summon(Character):
    def __init__(
        self,
        slot: int,
        caster_level: int,
        weapon: Weapon,
        bonus_dmg: int,
        feats=[],
        **kwargs
    ):
        base_feats = []
        base_feats.append(SummonAction(slot, weapon))
        base_feats.append(SummonHit(slot, bonus_dmg))
        base_feats.extend(feats)
        super().init(
            level=caster_level,
            stats=[10, 10, 10, 10, 10, 10],
            base_feats=base_feats,
            feats=[],
            feat_schedule=[],
        )


class FeyWeapon(Weapon):
    def __init__(self, **kwargs):
        super().__init__(name="FeyWeapon", num_dice=2, die=6, **kwargs)


class Mirthful(Feat):
    def __init__(self) -> None:
        self.name = "Mirthful"

    def begin_turn(self, target: Target):
        self.used = False

    def roll_attack(self, args: AttackRollArgs):
        if not self.used:
            args.adv = True
            self.used = True


class FeySummon(Summon):
    def __init__(self, slot: int, caster_level: int, to_hit: int):
        super().__init__(
            caster_level=caster_level,
            slot=slot,
            to_hit=to_hit,
            bonus_dmg=3,
            weapon=FeyWeapon(bonus=3 + slot),
            feats=[Mirthful()],
        )


class SummonSpell(Spell):
    def __init__(self, name: str, slot: int, caster_level: int, to_hit: int):
        super().__init__(name, slot, concentration=True)
        self.caster_level = caster_level
        self.to_hit = to_hit

    def summon(self):
        return None

    def begin(self, character):
        self.minion = self.summon()
        character.add_minion(self.minion)
        self.character = character

    def end(self):
        if self.character is not None:
            self.character.remove_minion(self.minion)


class SummonFey(SummonSpell):
    def __init__(self, slot: int, caster_level: int, to_hit: int):
        super().__init__(
            "SummonFey",
            slot,
            caster_level=caster_level,
            to_hit=to_hit,
        )

    def summon(self):
        return FeySummon(
            caster_level=self.caster_level, slot=self.slot, to_hit=self.to_hit
        )

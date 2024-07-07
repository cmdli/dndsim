from events import AttackArgs, AttackRollArgs, HitArgs
from target import Target
from util import (
    magic_weapon,
    roll_dice,
)
from character import Character
from feats import (
    ASI,
    Archery,
    CrossbowExpert,
    Feat,
    Spellcasting,
    EquipWeapon,
)
from weapons import HandCrossbow, Weapon
from spells import HuntersMark
from summons import FeySummon, SummonFey
from log import log


class RangerAction(Feat):
    def __init__(self, attacks) -> None:
        self.name = "RangerAction"
        self.attacks = attacks

    def action(self, target: Target):
        spellcasting = self.character.feat("Spellcasting")
        slot = spellcasting.highest_slot()
        if slot >= 4 and not spellcasting.is_concentrating():
            spell = SummonFey(
                slot,
                caster_level=self.character.level,
                to_hit=self.character.prof + self.character.mod("wis"),
            )
            spellcasting.cast(spell)
        else:
            if not spellcasting.is_concentrating() and self.character.use_bonus(
                "HuntersMark"
            ):
                spellcasting.cast(HuntersMark(slot))
            for weapon in self.attacks:
                log.record("main attack", 1)
                self.character.attack(target, weapon, main_action=True)


class HuntersMarkFeat(Feat):
    def __init__(self, die: int, adv: bool = False) -> None:
        self.name = "HuntersMarkFeat"
        self.die = die
        self.adv = adv

    def roll_attack(self, args: AttackRollArgs):
        spellcasting = self.character.feat("Spellcasting")
        if not spellcasting.concentrating_on("HuntersMark"):
            return
        if self.adv:
            args.adv = True

    def hit(self, args: HitArgs):
        spellcasting = self.character.feat("Spellcasting")
        if not spellcasting.concentrating_on("HuntersMark"):
            return
        num = 2 if args.crit else 1
        args.add_damage("HuntersMark", roll_dice(num, self.die))


class Gloomstalker(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.name = "Gloomstalker"
        self.weapon = weapon
        self.using = False
        self.first_turn = False
        self.used = False

    def short_rest(self):
        self.first_turn = True
        self.used = False

    def begin_turn(self, target: Target):
        self.used_attack = False

    def attack(self, args: AttackArgs):
        self.used_attack = True

    def hit(self, args: HitArgs):
        if self.using:
            num = 2 if args.crit else 1
            args.add_damage("Gloomstalker", roll_dice(num, 8))

    def end_turn(self, target):
        if self.first_turn and self.used_attack:
            self.using = True
            log.record("gloom attack", 1)
            self.character.attack(target, self.weapon)
            self.using = False
        self.first_turn = False
        self.used_attack = False


class Ranger(Character):
    def __init__(self, level):
        self.magic_weapon = magic_weapon(level)
        base_feats = []
        base_feats.append(Archery())
        weapon = HandCrossbow(bonus=self.magic_weapon)
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(EquipWeapon(weapon))
        base_feats.append(RangerAction(attacks=attacks))
        base_feats.append(Spellcasting(level, half=True))
        if level >= 20:
            base_feats.append(HuntersMarkFeat(10, True))
        elif level >= 17:
            base_feats.append(HuntersMarkFeat(6, True))
        else:
            base_feats.append(HuntersMarkFeat(6, False))
        if level >= 3:
            base_feats.append(Gloomstalker(weapon))
        base_feats.append(FeySummon())
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            feats=[
                CrossbowExpert(weapon),
                ASI([["dex", 2]]),
                ASI([["wis", 2]]),
                ASI([["wis", 2]]),
                ASI(),
            ],
            base_feats=base_feats,
        )

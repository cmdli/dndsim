from events import AttackArgs, AttackRollArgs, HitArgs, MissArgs
from target import Target
from util import (
    roll_dice,
    prof_bonus,
    get_magic_weapon,
)
from character import Character
from feats import (
    ASI,
    Archery,
    CrossbowExpert,
    Feat,
    Spellcasting,
    EquipWeapon, DualWielder,
)
from weapons import HandCrossbow, Weapon, Shortsword, Scimitar, Rapier
from spells import HuntersMark
from summons import FeySummon, SummonFey
from log import log


class RangerAction(Feat):
    def __init__(self, attacks, summon_fey: int = None) -> None:
        self.name = "RangerAction"
        self.attacks = attacks
        self.summon_fey = summon_fey

    def action(self, target: Target):
        spellcasting = self.character.feat("Spellcasting")
        slot = spellcasting.highest_slot()
        if self.summon_fey and slot >= self.summon_fey and not spellcasting.is_concentrating():
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
            for weapon in self.attacks():
                log.record("main attack", 1)
                self.character.attack(target, weapon, tags=["main_action"])


class HuntersMarkFeat(Feat):
    def __init__(self, die: int, adv: bool = False, filter=None) -> None:
        self.name = "HuntersMarkFeat"
        self.die = die
        self.adv = adv
        self.filter = filter

    def roll_attack(self, args: AttackRollArgs):
        spellcasting = self.character.feat("Spellcasting")
        if not spellcasting.concentrating_on("HuntersMark"):
            return
        if args.attack.weapon.is_other_creature:
            return
        if self.adv:
            args.adv = True

    def hit(self, args: HitArgs):
        spellcasting = self.character.feat("Spellcasting")
        if not spellcasting.concentrating_on("HuntersMark"):
            return
        if self.filter and not self.filter(args):
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


class BeastMaul(Weapon):
    def __init__(self, base, **kwargs):
        super().__init__(
            name="Beast Maul", num_dice=1, die=8, mod="wis", base=base, is_other_creature=True, **kwargs
        )


class BeastChargeFeat(Feat):
    def __init__(self, character: Character):
        self.name = "BeastChargeFeat"
        self.character = Character

    def hit(self, args: HitArgs):
        if isinstance(args.attack.weapon, BeastMaul):
            num = 2 if args.crit else 1
            args.add_damage("Charge", roll_dice(num, 6))
            if not args.attack.target.prone and not args.attack.target.save(self.character.dc("wis")):
                args.attack.target.prone = True
                log.output(lambda: "Knocked prone by Charge")


class StalkersFlurry(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.name = "StalkersFlurry"
        self.weapon = weapon

    def begin_turn(self, target: Target):
        self.missed_attack = False

    def miss(self, args: MissArgs):
        self.missed_attack = True

    def after_action(self, target):
        if self.missed_attack:
            self.character.attack(target, self.weapon)


class GloomstalkerRanger(Character):
    def __init__(self, level):
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        base_feats.append(Archery())
        weapon = HandCrossbow(bonus=magic_weapon)
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(EquipWeapon(weapon))
        base_feats.append(RangerAction(attacks=lambda: attacks, summon_fey=4))
        base_feats.append(Spellcasting(level, half=True))
        if level >= 20:
            base_feats.append(HuntersMarkFeat(10, True, ))
        elif level >= 17:
            base_feats.append(HuntersMarkFeat(6, True, ))
        else:
            base_feats.append(HuntersMarkFeat(6, False, ))
        if level >= 3:
            base_feats.append(Gloomstalker(weapon))
        if level >= 11:
            base_feats.append(StalkersFlurry(weapon))
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


class BeastMasterRanger(Character):
    def __init__(self, level):
        self.magic_weapon = get_magic_weapon(level)
        base_feats = []
        maul = BeastMaul(base=2 + prof_bonus(level))
        shortsword = Shortsword(bonus=self.magic_weapon)
        rapier = Rapier(bonus = self.magic_weapon)
        other_shortsword = Shortsword(bonus=self.magic_weapon, name="Offhand Shortsword", base="dex" if level >= 2 else 0)
        scimitar = Scimitar(bonus=self.magic_weapon, base="dex" if level >= 2 else 0)
        base_feats.append(EquipWeapon(maul))
        base_feats.append(EquipWeapon(shortsword))
        base_feats.append(EquipWeapon(rapier))
        base_feats.append(EquipWeapon(scimitar))
        base_feats.append(EquipWeapon(other_shortsword))
        def attacks():
            if self.has_feat("DualWielder"):
                main_weapon = rapier
            else:
                main_weapon = shortsword

            if self.level >= 3:
                if self.use_bonus("beast"):
                    yield maul
                    if level >= 11:
                        yield maul
                    yield main_weapon
                    yield main_weapon
                    yield scimitar
                else:
                    if level >= 5:
                        yield maul
                        if level >= 11:
                            yield maul
                        yield main_weapon
                        yield scimitar
                    else:
                        yield main_weapon
                        yield scimitar
            else:
                yield main_weapon
                if self.use_bonus("light weapon"):
                    yield other_shortsword
                else:
                    yield scimitar
        base_feats.append(RangerAction(attacks=attacks))
        base_feats.append(Spellcasting(level, half=True))
        base_feats.append(BeastChargeFeat(character=self))

        def beast_only_level_11(args: HitArgs) -> bool:
            return (not isinstance(args.attack.weapon, BeastMaul)) or (level >= 11)

        if level >= 20:
            base_feats.append(HuntersMarkFeat(10, True, ))
        elif level >= 17:
            base_feats.append(HuntersMarkFeat(6, True, ))
        else:
            base_feats.append(HuntersMarkFeat(6, False, filter=beast_only_level_11))
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            feats=[
                DualWielder(),
                ASI([["dex", 2]]),
                ASI([["wis", 2]]),
                ASI([["wis", 2]]),
                ASI(),
            ],
            base_feats=base_feats,
        )

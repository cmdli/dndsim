from typing import List, override, Optional

from sim.events import AttackArgs, AttackResultArgs, AttackRollArgs
from sim.target import Target
from util.util import (
    roll_dice,
    get_magic_weapon,
)
from sim.character import Character
from sim.feats import (
    ASI,
    Archery,
    CrossbowExpert,
    Feat,
    DualWielder,
    TwoWeaponFighting,
    WeaponMasteries,
    IrresistibleOffense,
)
from sim.weapons import HandCrossbow, Weapon, Shortsword, Scimitar, Rapier
from spells.ranger import HuntersMark
from sim.spellcasting import Spellcaster
from sim.summons import SummonFey
from util.log import log


def maybe_cast_summon_fey(character: Character, summon_fey_threshold: int):
    slot = character.spells.highest_slot()
    if (
        summon_fey_threshold
        and slot >= summon_fey_threshold
        and not character.spells.is_concentrating()
    ):
        spell = SummonFey(slot)
        character.spells.cast(spell)
        return True
    return False


def maybe_cast_hunters_mark(character: Character):
    slot = character.spells.lowest_slot()
    if (
        slot > 0
        and not character.spells.is_concentrating()
        and character.use_bonus("HuntersMark")
    ):
        character.spells.cast(HuntersMark(slot))
        return True
    return False


class RangerAction(Feat):
    def __init__(self, attacks, summon_fey_threshold: int) -> None:
        self.attacks = attacks
        self.summon_fey_threshold = summon_fey_threshold

    def action(self, target: Target):
        if maybe_cast_summon_fey(self.character, self.summon_fey_threshold):
            return
        maybe_cast_hunters_mark(self.character)
        for weapon in self.attacks:
            log.record("main attack", 1)
            self.character.weapon_attack(target, weapon, tags=["main_action"])


class HuntersMarkFeat(Feat):
    def __init__(
        self,
        die: int,
        caster: Optional[Character] = None,
        adv: bool = False,
    ) -> None:
        self.die = die
        self.adv = adv
        self.caster = caster
        self.filter = filter

    def apply(self, character: Character):
        super().apply(character)
        if self.caster is None:
            self.caster = character

    def attack_roll(self, args: AttackRollArgs):
        if self.caster.spells.concentrating_on("HuntersMark") and self.adv:
            args.adv = True

    def attack_result(self, args):
        if args.hits() and self.caster.spells.concentrating_on("HuntersMark"):
            args.add_damage_dice("HuntersMark", 1, self.die)


class Gloomstalker(Feat):
    def __init__(self, weapon: Weapon) -> None:
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

    def attack_result(self, args):
        if args.hits() and self.using:
            args.add_damage_dice("Gloomstalker", 1, 8)

    def end_turn(self, target):
        if self.first_turn and self.used_attack:
            self.using = True
            log.record("gloom attack", 1)
            self.character.weapon_attack(target, self.weapon)
            self.using = False
        self.first_turn = False
        self.used_attack = False


class DreadAmbusher(Feat):
    def __init__(self, level: int, weapon: Weapon) -> None:
        self.die = 8 if level >= 11 else 6
        self.weapon = weapon if level >= 11 else None

    def apply(self, character: Character):
        super().apply(character)
        self.max_uses = character.mod("wis")
        self.uses = self.max_uses

    def long_rest(self):
        self.uses = self.max_uses

    def begin_turn(self, target: Target):
        self.used = False

    def attack_result(self, args):
        if args.hits() and not self.used and self.uses > 0:
            self.used = True
            self.uses -= 1
            args.add_damage_dice("DreadAmbusher", 2, self.die)
            if self.weapon:
                self.character.weapon_attack(args.attack.target, self.weapon)


class BeastChargeFeat(Feat):
    def __init__(self, character: "Character"):
        self.character = character

    def attack_result(self, args):
        if args.hits() and isinstance(args.attack.weapon, BeastMaul):
            args.add_damage_dice("Charge", 1, 6)
            if not args.attack.target.prone and not args.attack.target.save(
                self.character.dc("wis")
            ):
                args.attack.target.prone = True
                log.output(lambda: "Knocked prone by Charge")


class StalkersFlurry(Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.weapon = weapon

    def begin_turn(self, target: Target):
        self.missed_attack = False

    def attack_result(self, args):
        if args.misses():
            self.missed_attack = True

    def after_action(self, target):
        if self.missed_attack:
            self.character.weapon_attack(target, self.weapon)


class GloomstalkerRanger(Character):
    def __init__(self, level, **kwargs):
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        base_feats.append(WeaponMasteries(["vex", "nick"]))
        if level >= 2:
            base_feats.append(Archery())
        weapon = HandCrossbow(magic_bonus=magic_weapon)
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(RangerAction(attacks=attacks, summon_fey_threshold=4))
        base_feats.append(
            HuntersMarkFeat(die=10 if level >= 20 else 6, adv=level >= 17)
        )
        if level >= 3:
            base_feats.append(DreadAmbusher(level, weapon))
        if level >= 4:
            base_feats.append(CrossbowExpert(weapon))
        if level >= 8:
            base_feats.append(ASI(["dex"]))
        if level >= 12:
            base_feats.append(ASI(["wis"]))
        if level >= 16:
            base_feats.append(ASI(["wis"]))
        if level >= 19:
            base_feats.append(IrresistibleOffense("dex"))
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            base_feats=base_feats,
            spell_mod="wis",
            spellcaster=Spellcaster.HALF,
        )


class PrimalCompanion(Character):
    def __init__(self, level: int, ranger: Character, **kwargs):
        self.ranger = ranger
        self.num_attacks = 2 if level >= 11 else 1
        self.weapon = BeastMaul(self)
        base_feats: List[Feat] = [BeastChargeFeat(ranger)]
        if level >= 11:
            base_feats += [HuntersMarkFeat(die=10 if level >= 20 else 6, caster=ranger)]
        super().init(
            level=level,
            stats=[10, 10, 10, 10, 10, 10],
            base_feats=base_feats,
        )

    def do_attack(self, target: Target):
        for _ in range(self.num_attacks):
            self.weapon_attack(target, self.weapon)

    def get_to_hit(self):
        return self.ranger.prof + self.ranger.mod("wis")


class BeastMaul(Weapon):
    def __init__(self, ranger: Character, **kwargs):
        super().__init__(name="Beast Maul", num_dice=1, die=8, **kwargs)
        self.ranger = ranger

    @override
    def to_hit(self, character):
        return self.ranger.prof + self.ranger.mod("wis")

    @override
    def attack_result(self, args: AttackResultArgs, character: Character):
        if not args.hits():
            return
        num_dice = 2 if args.crit else 1
        args.add_damage(self.name(), num_dice * [8], 2 + self.ranger.mod("wis"))


class BeastMasterAction(Feat):
    def __init__(
        self,
        beast: PrimalCompanion,
        main_hand: Weapon,
        off_hand_nick: Weapon,
        off_hand_other: Weapon,
    ) -> None:
        self.beast = beast
        self.off_hand_other = off_hand_other
        self.off_hand_nick = off_hand_nick
        self.main_hand = main_hand

    def action(self, target: Target):
        if maybe_cast_summon_fey(self.character, summon_fey_threshold=4):
            return
        maybe_cast_hunters_mark(self.character)
        if self.character.level >= 3:
            commanded_beast = False
            if self.character.use_bonus("beast"):
                log.output(lambda: "Use bonus action for beast attack")
                self.beast.do_attack(target)
                commanded_beast = True
            num_attacks = 2 if self.character.level >= 5 else 1
            for _ in range(num_attacks):
                if not commanded_beast:
                    self.beast.do_attack(target)
                    commanded_beast = True
                else:
                    self.character.weapon_attack(target, self.main_hand)
            self.character.weapon_attack(target, self.off_hand_nick, tags=["light"])
        else:
            self.character.weapon_attack(target, self.main_hand)
            if self.character.use_bonus("light weapon"):
                self.character.weapon_attack(
                    target, self.off_hand_other, tags=["light"]
                )
            else:
                self.character.weapon_attack(target, self.off_hand_nick, tags=["light"])


class BeastMasterRanger(Character):
    def __init__(self, level, **kwargs):
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        base_feats.append(WeaponMasteries(["vex", "nick"]))
        beast = PrimalCompanion(level, ranger=self)
        shortsword = Shortsword(magic_bonus=magic_weapon)
        rapier = Rapier(magic_bonus=magic_weapon)
        other_shortsword = Shortsword(
            magic_bonus=magic_weapon,
            name="OffhandShortsword",
        )
        scimitar = Scimitar(magic_bonus=magic_weapon)
        if level >= 2:
            base_feats.append(TwoWeaponFighting())
        if level >= 4:
            base_feats.append(DualWielder("dex", shortsword))
        if level >= 8:
            base_feats.append(ASI(["dex"]))
        if level >= 12:
            base_feats.append(ASI(["wis"]))
        if level >= 16:
            base_feats.append(ASI(["wis"]))
        if level >= 19:
            base_feats.append(IrresistibleOffense("dex"))
        base_feats.append(
            HuntersMarkFeat(die=10 if level >= 20 else 6, adv=level >= 17)
        )
        base_feats.append(
            BeastMasterAction(
                beast=beast,
                main_hand=rapier if level >= 4 else shortsword,
                off_hand_nick=scimitar,
                off_hand_other=other_shortsword,
            )
        )
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            base_feats=base_feats,
            spellcaster=Spellcaster.HALF,
            spell_mod="wis",
        )
        self.add_minion(beast)

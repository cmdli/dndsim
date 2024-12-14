from typing import List, override, Optional

from sim.events import AttackArgs, AttackResultArgs, AttackRollArgs
from util.util import get_magic_weapon
from feats import (
    ASI,
    Archery,
    CrossbowExpert,
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

import sim.feat
import sim.character
import sim.target
import sim.weapons


def maybe_cast_summon_fey(
    character: "sim.character.Character", summon_fey_threshold: int
):
    slot = character.spells.highest_slot()
    if slot >= summon_fey_threshold and not character.spells.is_concentrating():
        spell = SummonFey(slot)
        character.spells.cast(spell)
        return True
    return False


def maybe_cast_hunters_mark(character: "sim.character.Character"):
    slot = character.spells.lowest_slot()
    if (
        slot > 0
        and not character.spells.is_concentrating()
        and character.use_bonus("HuntersMark")
    ):
        character.spells.cast(HuntersMark(slot))
        return True
    return False


class RangerAction(sim.feat.Feat):
    def __init__(
        self, attacks: List["sim.weapons.Weapon"], summon_fey_threshold: int
    ) -> None:
        self.attacks = attacks
        self.summon_fey_threshold = summon_fey_threshold

    def action(self, target: "sim.target.Target"):
        if maybe_cast_summon_fey(self.character, self.summon_fey_threshold):
            return
        maybe_cast_hunters_mark(self.character)
        for weapon in self.attacks:
            self.character.weapon_attack(target, weapon, tags=["main_action"])


class HuntersMarkFeat(sim.feat.Feat):
    def __init__(
        self,
        die: int,
        caster: Optional["sim.character.Character"] = None,
    ) -> None:
        self.die = die
        self.caster = caster

    def apply(self, character: "sim.character.Character"):
        super().apply(character)
        if self.caster is None:
            self.caster = character

    def attack_result(self, args):
        if args.hits() and self.caster.spells.concentrating_on("HuntersMark"):
            args.add_damage(source="HuntersMark", dice=[self.die])


class PreciseHunter(sim.feat.Feat):
    def attack_roll(self, args: AttackRollArgs):
        if args.attack.target.has_tag("HuntersMark"):
            args.adv = True


class Gloomstalker(sim.feat.Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.weapon = weapon
        self.using = False
        self.first_turn = False
        self.used = False

    def short_rest(self):
        self.first_turn = True
        self.used = False

    def begin_turn(self, target: "sim.target.Target"):
        self.used_attack = False

    def attack(self, args: AttackArgs):
        self.used_attack = True

    def attack_result(self, args):
        if args.hits() and self.using:
            args.add_damage(source="Gloomstalker", dice=[8])

    def end_turn(self, target):
        if self.first_turn and self.used_attack:
            self.using = True
            log.record("gloom attack", 1)
            self.character.weapon_attack(target, self.weapon)
            self.using = False
        self.first_turn = False
        self.used_attack = False


class DreadAmbusher(sim.feat.Feat):
    def __init__(self, level: int, weapon: Weapon) -> None:
        self.die = 8 if level >= 11 else 6
        self.weapon = weapon if level >= 11 else None

    def apply(self, character: "sim.character.Character"):
        super().apply(character)
        self.max_uses = character.mod("wis")
        self.uses = self.max_uses

    def long_rest(self):
        self.uses = self.max_uses

    def begin_turn(self, target: "sim.target.Target"):
        self.used = False

    def attack_result(self, args):
        if args.hits() and not self.used and self.uses > 0:
            self.used = True
            self.uses -= 1
            args.add_damage(source="DreadAmbusher", dice=2 * [self.die])
            if self.weapon:
                self.character.weapon_attack(args.attack.target, self.weapon)


class BeastChargeFeat(sim.feat.Feat):
    def __init__(self, character: "sim.character.Character"):
        self.character = character

    def attack_result(self, args):
        if args.hits() and isinstance(args.attack.weapon, BeastMaul):
            args.add_damage(source="Charge", dice=[6])
            if not args.attack.target.prone and not args.attack.target.save(
                self.character.dc("wis")
            ):
                args.attack.target.knock_prone()


class StalkersFlurry(sim.feat.Feat):
    def __init__(self, weapon: Weapon) -> None:
        self.weapon = weapon

    def begin_turn(self, target: "sim.target.Target"):
        self.missed_attack = False

    def attack_result(self, args):
        if args.misses():
            self.missed_attack = True

    def after_action(self, target):
        if self.missed_attack:
            self.character.weapon_attack(target, self.weapon)


class GloomstalkerRanger(sim.character.Character):
    def __init__(self, level, **kwargs):
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        base_feats.append(WeaponMasteries(["vex", "nick"]))
        weapon = HandCrossbow(magic_bonus=magic_weapon)
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(RangerAction(attacks=attacks, summon_fey_threshold=4))
        base_feats.append(HuntersMarkFeat(die=10 if level >= 20 else 6))
        if level >= 2:
            base_feats.append(Archery())
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
        if level >= 17:
            base_feats.append(PreciseHunter())
        if level >= 19:
            base_feats.append(IrresistibleOffense("dex"))
        super().init(
            level=level,
            stats=[10, 17, 10, 10, 16, 10],
            base_feats=base_feats,
            spell_mod="wis",
            spellcaster=Spellcaster.HALF,
        )


class PrimalCompanion(sim.character.Character):
    def __init__(self, level: int, ranger: "sim.character.Character", **kwargs):
        self.ranger = ranger
        self.num_attacks = 2 if level >= 11 else 1
        self.weapon = BeastMaul(self)
        base_feats: List[sim.feat.Feat] = [BeastChargeFeat(ranger)]
        if level >= 11:
            base_feats.append(
                HuntersMarkFeat(die=10 if level >= 20 else 6, caster=ranger)
            )
        super().init(
            level=level,
            stats=[10, 10, 10, 10, 10, 10],
            base_feats=base_feats,
        )

    def do_attack(self, target: "sim.target.Target"):
        for _ in range(self.num_attacks):
            self.weapon_attack(target, self.weapon)

    def get_to_hit(self):
        return self.ranger.prof + self.ranger.mod("wis")


class BeastMaul(Weapon):
    def __init__(self, ranger: "sim.character.Character", **kwargs):
        super().__init__(name="Beast Maul", num_dice=1, die=8, **kwargs)
        self.ranger = ranger

    @override
    def to_hit(self, character):
        return self.ranger.prof + self.ranger.mod("wis")

    @override
    def attack_result(
        self, args: AttackResultArgs, character: "sim.character.Character"
    ):
        if not args.hits():
            return
        num_dice = 2 if args.crit else 1
        args.add_damage(self.name(), num_dice * [8], 2 + self.ranger.mod("wis"))


class BeastMasterAction(sim.feat.Feat):
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

    def action(self, target: "sim.target.Target"):
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


class BeastMasterRanger(sim.character.Character):
    def __init__(self, level, **kwargs):
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        base_feats.append(WeaponMasteries(["vex", "nick"]))
        base_feats.append(HuntersMarkFeat(die=10 if level >= 20 else 6))
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
        if level >= 17:
            base_feats.append(PreciseHunter())
        if level >= 19:
            base_feats.append(IrresistibleOffense("dex"))
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

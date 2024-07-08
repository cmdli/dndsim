from typing import List

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


# ranger casts either summon fey or hunter's mark, returns true if ranger still has action
def cast_spell(character: Character, summon_fey: int) -> bool:
    spellcasting = character.feat("Spellcasting")
    slot = spellcasting.highest_slot()
    if summon_fey and slot >= summon_fey and not spellcasting.is_concentrating():
        spell = SummonFey(
            slot,
            caster_level=character.level,
            to_hit=character.prof + character.mod("wis"),
        )
        spellcasting.cast(spell)
        return False
    else:
        if not spellcasting.is_concentrating() and character.use_bonus(
                "HuntersMark"
        ):
            spellcasting.cast(HuntersMark(slot))
        return True

class RangerAction(Feat):
    def __init__(self, attacks, summon_fey: int = None) -> None:
        self.name = "RangerAction"
        self.attacks = attacks
        self.summon_fey = summon_fey

    def action(self, target: Target):
        has_action = cast_spell(self.character, self.summon_fey)
        if has_action:
            for weapon in self.attacks:
                log.record("main attack", 1)
                self.character.attack(target, weapon, tags=["main_action"])


class HuntersMarkFeat(Feat):
    def __init__(self, die: int, adv: bool = False, caster: Character = None) -> None:
        self.name = "HuntersMarkFeat"
        self.die = die
        self.adv = adv
        self.filter = filter
        self.caster = caster

    def roll_attack(self, args: AttackRollArgs):
        spellcasting = (self.caster or self.character).feat("Spellcasting")
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


class BeastChargeFeat(Feat):
    def __init__(self):
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
        base_feats.append(RangerAction(attacks=attacks, summon_fey=4))
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

class PrimalCompanion(Character):
    def __init__(self, level: int, ranger: Character, attack: Weapon):
        self.ranger = ranger
        base_feats: List[Feat] = [
            BeastChargeFeat(),
            EquipWeapon(attack)
        ]
        if level >= 11:
            base_feats += [HuntersMarkFeat(die=10 if level >= 20 else 6, caster=ranger)]
        super().init(
            level=level,
            stats=[10, 10, 10, 10, 10, 10],
            feats=[],
            base_feats=base_feats,
        )


class BeastMaul(Weapon):
    def __init__(self, base, **kwargs):
        super().__init__(
            name="Beast Maul", num_dice=1, die=8, mod="wis", base=base, **kwargs
        )


class BeastMasterAction(Feat):
    def __init__(self, beast: Character, maul: Weapon, main_hand: Weapon, off_hand_nick: Weapon, off_hand_other: Weapon) -> None:
        self.maul = maul
        self.beast = beast
        self.off_hand_other = off_hand_other
        self.off_hand_nick = off_hand_nick
        self.main_hand = main_hand
        self.name = "BeastMasterAction"

    def action(self, target: Target):
        has_action = cast_spell(self.character, None)
        if has_action:
            if self.character.level >= 3:
                if self.character.use_bonus("beast"):
                    log.output(lambda: "Use bonus action for beast attack")
                    self.beast.attack(target, self.maul)
                    if self.character.level >= 11:
                        self.beast.attack(target, self.maul)
                    self.character.attack(target, self.main_hand)
                else:
                    if self.character.level >= 5:
                        self.beast.attack(target, self.maul)
                        if self.character.level >= 11:
                            self.beast.attack(target, self.maul)
                self.character.attack(target, self.main_hand)
                self.character.attack(target, self.off_hand_nick)
            else:
                self.character.attack(target, self.main_hand)
                tags = [] if self.character.level >= 2 else ["light"]
                if self.character.use_bonus("light weapon"):
                    self.character.attack(target, self.off_hand_other, tags=tags)
                else:
                    self.character.attack(target, self.off_hand_nick, tags=tags)


class BeastMasterRanger(Character):
    def __init__(self, level):
        self.magic_weapon = get_magic_weapon(level)
        base_feats = []
        maul = BeastMaul(base=2 + prof_bonus(level))
        beast = PrimalCompanion(level, self, attack=maul)
        shortsword = Shortsword(bonus=self.magic_weapon)
        rapier = Rapier(bonus = self.magic_weapon)
        other_shortsword = Shortsword(
            bonus=self.magic_weapon,
            name="OffhandShortsword",
        )
        scimitar = Scimitar(bonus=self.magic_weapon)
        base_feats.append(EquipWeapon(maul))
        base_feats.append(EquipWeapon(shortsword))
        base_feats.append(EquipWeapon(rapier))
        base_feats.append(EquipWeapon(scimitar))
        base_feats.append(EquipWeapon(other_shortsword))
        base_feats.append(Spellcasting(level, half=True))
        base_feats.append(BeastChargeFeat())

        if level >= 20:
            base_feats.append(HuntersMarkFeat(10, True, ))
        elif level >= 17:
            base_feats.append(HuntersMarkFeat(6, True, ))
        else:
            base_feats.append(HuntersMarkFeat(6, False, ))
        base_feats.append(BeastMasterAction(
            beast=beast,
            maul=maul,
            main_hand=rapier if level >= 4 else shortsword,
            off_hand_nick=scimitar,
            off_hand_other=other_shortsword,
        ))
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
        self.add_minion(beast)

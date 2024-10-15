from sim.events import AttackRollArgs, HitArgs
from sim.target import Target
from util.util import (
    get_magic_weapon,
    roll_dice,
)
from sim.character import Character
from sim.feats import (
    ASI,
    AttackAction,
    GreatWeaponMaster,
    Feat,
    TwoWeaponFighting,
    GreatWeaponFighting,
    WeaponMasteries,
    IrresistibleOffense,
)
from sim.weapons import Greatsword, Shortsword, Scimitar
from spells.paladin import DivineFavor, DivineSmite
from sim.spellcasting import Spellcaster


class DivineSmiteFeat(Feat):
    def begin_turn(self, target: Target):
        self.used = False

    def hit(self, args: HitArgs):
        slot = self.character.spells.highest_slot()
        if not self.used and slot >= 1 and self.character.use_bonus("DivineSmite"):
            self.used = True
            self.character.spells.cast(
                DivineSmite(slot, args.crit), target=args.attack.target
            )


class ImprovedDivineSmite(Feat):
    def hit(self, args: HitArgs):
        num = 2 if args.crit else 1
        args.add_damage("ImprovedDivineSmite", roll_dice(num, 8))


class SacredWeapon(Feat):
    def short_rest(self):
        self.enabled = False

    def begin_turn(self, target: Target):
        if not self.enabled and self.character.use_bonus("SacredWeapon"):
            self.enabled = True

    def roll_attack(self, args: AttackRollArgs):
        if self.enabled:
            args.situational_bonus += self.character.mod("cha")


class DivineFavorFeat(Feat):
    def begin_turn(self, target: Target):
        slot = self.character.spells.lowest_slot()
        if (
            not self.character.spells.is_concentrating()
            and slot >= 1
            and self.character.use_bonus("DivineFavor")
        ):
            self.character.spells.cast(DivineFavor(slot))

    def hit(self, args: HitArgs):
        if self.character.spells.concentrating_on("DivineFavor"):
            args.add_damage("DivineFavor", roll_dice(1, 4))


class Paladin(Character):
    def __init__(self, level: int, use_twf=False, **kwargs):
        magic_weapon = get_magic_weapon(level)
        base_feats = []
        base_feats.append(DivineFavorFeat())
        if use_twf:
            base_feats.append(WeaponMasteries(["vex", "nick"]))
            scimitar = Scimitar(magic_bonus=magic_weapon)
            base_feats.append(TwoWeaponFighting())
            weapon = Shortsword(magic_bonus=magic_weapon)
            nick_attacks = [scimitar]
        else:
            base_feats.append(WeaponMasteries(["graze", "topple"]))
            base_feats.append(GreatWeaponFighting())
            weapon = Greatsword(magic_bonus=magic_weapon)
            nick_attacks = []
        if level >= 5:
            attacks = 2 * [weapon]
        else:
            attacks = [weapon]
        base_feats.append(AttackAction(attacks=attacks, nick_attacks=nick_attacks))
        if level >= 2:
            base_feats.append(DivineSmiteFeat())
        if level >= 3:
            base_feats.append(SacredWeapon())
        if level >= 4:
            if use_twf:
                base_feats.append(ASI(["str", "con"]))
            else:
                base_feats.append(GreatWeaponMaster(weapon))
        if level >= 8:
            base_feats.append(ASI(["str"]))
        if level >= 11:
            base_feats.append(ImprovedDivineSmite())
        if level >= 12:
            base_feats.append(ASI(["cha"]))
        if level >= 16:
            base_feats.append(ASI(["cha"]))
        if level >= 19:
            base_feats.append(IrresistibleOffense("str"))
        super().init(
            level=level,
            stats=[17, 10, 10, 10, 10, 16],
            base_feats=base_feats,
            spellcaster=Spellcaster.HALF,
        )

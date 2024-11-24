from sim.events import AttackRollArgs
from util.util import (
    prof_bonus,
    get_magic_weapon,
    cantrip_dice,
    highest_spell_slot,
    spell_slots,
    roll_dice,
    do_roll,
)
from util.log import log
from sim.target import Target
from sim.character import Character
from sim.spellcasting import Spellcaster
from sim.feat import Feat
from sim.events import AttackArgs
from spells.wizard import (
    MeteorSwarm,
    Fireball,
    Firebolt,
    MagicMissile,
    FingerOfDeath,
    Blight,
    ChainLightning,
    ScorchingRay,
)
from sim.summons import SummonFey
from sim.feats import ASI
from sim.spells import Spell
from typing import List


class Wizard:
    def __init__(self, level: int, **kwargs):
        self.level = level
        self.prof = prof_bonus(level)
        if level >= 8:
            self.int = 5
        elif level >= 4:
            self.int = 4
        else:
            self.int = 3
        self.dc = 8 + self.prof + self.int
        self.to_hit = self.prof + self.int + get_magic_weapon(level)
        self.cantrip_dice = cantrip_dice(level)
        self.long_rest()

    def long_rest(self):
        self.short_rest()
        self.slots = spell_slots(self.level)
        self.used_arcane_recovery = False
        self.used_overchannel = self.level < 14

    def short_rest(self):
        # TODO: use arcane recovery
        self.concentration = False
        self.fey_summon = 0

    def turn(self, target):
        slot = highest_spell_slot(self.slots)
        # if slot >= 3 and not self.concentration:
        #     self.fey_summon = slot
        #     self.concentration = True
        # else:
        #     if slot >= 9:
        #         self.meteor_swarm(target)
        #     elif slot >= 7:
        #         self.finger_of_death(target)
        #     elif slot >= 6:
        #         self.chain_lightning(target)
        #     elif slot >= 5 and not self.used_overchannel:
        #         self.blight(target, slot, overchannel=True)
        #         self.used_overchannel = True
        # if slot >= 4:
        #     self.blight(target, slot)
        # if slot >= 3:
        #     self.fireball(target, slot)
        # elif slot >= 2 and self.level < 11:
        #     self.scorching_ray(target, slot)
        # elif slot >= 1 and self.level < 5:
        #     self.magic_missile(target, slot)
        # else:
        self.firebolt(target)
        if slot >= 1:
            self.slots[slot] -= 1
        # if self.fey_summon > 0:
        #     self.summon_fey(target)

    def enemy_turn(self, target):
        pass

    def meteor_swarm(self, target):
        dmg = roll_dice(40, 6) + self.int
        if target.save(self.dc):
            target.damage(dmg // 2)
        else:
            target.damage(dmg)

    def finger_of_death(self, target):
        dmg = roll_dice(7, 8) + 30
        if target.save(self.dc):
            target.damage(dmg // 2)
        else:
            target.damage(dmg)

    def chain_lightning(self, target):
        dmg = roll_dice(10, 8) + self.int
        if target.save(self.dc):
            target.damage(dmg // 2)
        else:
            target.damage(dmg)

    def disintegrate(self, target, slot):
        if not target.save(self.dc):
            target.damage(40 + roll_dice(10 + (slot - 6), 6))

    def steel_wind_strike(self, target):
        roll = do_roll()
        if roll == 20:
            target.damage(roll_dice(12, 10))
        elif roll + self.to_hit >= target.ac:
            target.damage(roll_dice(6, 10))

    def blight(self, target, slot, overchannel=False):
        num_dice = 8 + (slot - 4)
        if overchannel:
            dmg = num_dice * 8
        else:
            dmg = roll_dice(num_dice, 8)
        if self.level >= 10:
            dmg += self.int
        if target.save(self.dc):
            target.damage(dmg // 2)
        else:
            target.damage(dmg)

    def scorching_ray(self, target, slot):
        for _ in range(1 + slot):
            roll = do_roll()
            if roll == 20:
                target.damage_source("ScorchingRay", roll_dice(4, 6))
            elif roll + self.to_hit >= target.ac:
                target.damage_source("ScorchingRay", roll_dice(2, 6))
        if self.level >= 10:
            target.damage_source("EmpoweredEvocation", self.int)

    def fireball(self, target, slot):
        dmg = roll_dice(5 + slot, 6)
        if self.level >= 10:
            dmg += self.int
        if not target.save(self.dc):
            target.damage(dmg)
        else:
            target.damage(dmg // 2)

    def erupting_earth(self, target, slot):
        dmg = roll_dice(3 + (slot - 3), 12)
        if target.save(self.dc):
            target.damage(dmg)
        else:
            target.damage(dmg // 2)

    def magic_missile(self, target, slot):
        target.damage_source("MagicMissile", roll_dice(2 + slot, 4) + 2 + slot)
        if self.level >= 10:
            target.damage_source("EmpoweredEvocation", self.int)

    def firebolt(self, target, adv=False):
        roll = do_roll(adv=adv)
        num_dice = self.cantrip_dice
        if roll == 20:
            log.record("Crit:Firebolt", 1)
            num_dice *= 2
        dmg = roll_dice(num_dice, 10)
        if self.level >= 10:
            dmg += self.int
        if roll + self.to_hit >= target.ac:
            log.record("Hit:Firebolt", 1)
            target.damage(dmg)
        elif self.level >= 2:
            target.damage(dmg // 2)

    def summon_fey(self, target):
        adv = True  # Advantage on first attack
        num_attacks = self.fey_summon // 2
        for _ in range(num_attacks):
            roll = do_roll(adv=adv)
            adv = False
            if roll == 20:
                target.damage(roll_dice(4, 6) + 3 + self.fey_summon)
            elif roll + self.to_hit >= target.ac:
                target.damage(roll_dice(2, 6) + 3 + self.fey_summon)


class WandOfTheWarMage(Feat):
    def __init__(self, bonus: int) -> None:
        super().__init__()
        self.bonus = bonus

    def roll_attack(self, args: AttackRollArgs):
        if args.attack.weapon.spell != None:
            args.situational_bonus += self.bonus


class PotentCantrip(Feat):
    # TODO: Add damage when enemy saves against a cantrip
    def attack_result(self, args):
        weapon = args.attack.weapon
        if args.misses() and weapon.spell is not None and weapon.spell.slot == 0:
            damage = weapon.damage(
                self.character,
                args.attack,
                crit=False,
            )
            args.add_flat_damage("PotentCantrip", damage // 2)


class WizardAction(Feat):
    def action(self, target: Target):
        slot = self.character.spells.highest_slot()
        spell: Spell = None
        # if slot >= 3 and not self.character.spells.is_concentrating():
        #     spell = SummonFey(slot)
        # elif slot >= 9:
        #     spell = MeteorSwarm(slot)
        # elif slot >= 7:
        #     spell = FingerOfDeath(slot)
        # elif slot >= 6:
        #     spell = ChainLightning(slot)
        # if slot >= 4:
        #     spell = Blight(slot)
        # if slot >= 3:
        #     spell = Fireball(slot)
        # elif slot >= 2 and self.character.level < 11:
        #     spell = ScorchingRay(slot)
        # elif slot >= 1 and self.character.level < 5:
        #     spell = MagicMissile(slot)
        # else:
        spell = Firebolt()
        if spell is not None:
            self.character.spells.cast(spell, target)


class Wizard2(Character):
    def __init__(self, level: int) -> None:
        magic_weapon = get_magic_weapon(level)
        feats: List[Feat] = []
        feats.append(WizardAction())
        feats.append(WandOfTheWarMage(magic_weapon))
        if level >= 3:
            feats.append(PotentCantrip())
        if level >= 4:
            feats.append(ASI(["int"]))
        if level >= 8:
            feats.append(ASI(["int", "wis"]))
        super().init(
            level=level,
            stats=[10, 10, 10, 17, 10, 10],
            base_feats=feats,
            spellcaster=Spellcaster.FULL,
            spell_mod="int",
        )

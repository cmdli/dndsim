from events import AttackRollArgs, HitArgs
from feats import Feat
from util import do_roll, roll_dice
from target import Target
from log import log


class Summon(Feat):
    def __init__(
        self,
        name: str,
        spell_name: str,
        num_dice: int = 0,
        die: int = 6,
        base_dmg: int = 0,
        mod: str = "wis",
    ) -> None:
        self.name = name
        self.spell_name = spell_name
        self.num_dice = num_dice
        self.die = die
        self.base_dmg = base_dmg
        self.mod = mod

    def end_turn(self, target):
        spellcasting = self.character.feat("Spellcasting")
        if not spellcasting.concentrating_on(self.spell_name):
            return
        self.summon_action(target)

    def summon_begin_turn(self):
        pass

    def summon_action(self, target: Target):
        log.record("Summon Action", 1)
        self.summon_begin_turn()
        spellcasting = self.character.feat("Spellcasting")
        slot = spellcasting.concentration.slot
        for _ in range(slot // 2):
            to_hit = self.character.prof + self.character.mod(self.mod)
            roll = self.summon_roll_attack()
            if roll == 20:
                self.summon_hit(slot, target, crit=True)
            elif roll + to_hit >= target.ac:
                self.summon_hit(slot, target)

    def summon_roll_attack(self):
        return do_roll()

    def summon_hit(self, slot: int, target: Target, crit: bool = False):
        num = self.num_dice
        if crit:
            num *= 2
        target.damage_source(self.name, roll_dice(num, self.die) + self.base_dmg + slot)


class FeySummon(Summon):
    def __init__(self):
        super().__init__(
            name="FeySummon",
            spell_name="SummonFey",
            num_dice=2,
            die=6,
            base_dmg=3,
            mod="wis",
        )

    def summon_begin_turn(self):
        self.adv_used = False

    def summon_roll_attack(self):
        roll = do_roll(adv=not self.adv_used)
        self.adv_used = True
        return roll

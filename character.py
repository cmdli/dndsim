from util import prof_bonus
from feats import Attack, Vex, Feat
from target import Target
from weapons import Weapon
from events import HitArgs, AttackRollArgs, AttackArgs, MissArgs
from log import log
from typing import List
from collections import defaultdict
from util import spell_slots, highest_spell_slot, lowest_spell_slot
from spells import Spell, Spellcaster
from typing import Callable, Any


class Character:
    def init(
        self,
        level=None,
        stats=None,
        feats=None,
        base_feats: List[Feat] = None,
        feat_schedule=[4, 8, 12, 16, 19],
        default_feats=None,
        spellcaster: Spellcaster = Spellcaster.NONE,
        spell_mod: str = None,
    ):
        if default_feats is None:
            default_feats = [Attack(), Vex()]
        self.level = level
        self.prof = prof_bonus(level)
        self.str = stats[0]
        self.dex = stats[1]
        self.con = stats[2]
        self.int = stats[3]
        self.wis = stats[4]
        self.cha = stats[5]
        self.minions = []
        self.effects = set()
        self.spellcaster = spellcaster
        self.spell_mod = spell_mod
        self.concentration = None
        self.feats = dict()
        self.feats_by_event = dict()
        for feat in default_feats:
            self.add_feat(feat)
        for feat in base_feats:
            self.add_feat(feat)
        for [target, feat] in zip(feat_schedule, feats):
            if level >= target:
                self.add_feat(feat)

    def add_feat(self, feat):
        feat.apply(self)
        self.feats[feat.name] = feat
        for event in feat.events():
            if event not in self.feats_by_event:
                self.feats_by_event[event] = []
            self.feats_by_event[event].append(feat)

    def has_feat(self, name: str):
        return name in self.feats

    def feat(self, name: str):
        return self.feats[name]

    def feats_for_event(self, event: str):
        if event not in self.feats_by_event:
            return []
        return self.feats_by_event[event]

    def has_feats_for_event(self, event: str):
        return event in self.feats_by_event

    def mod(self, stat: str):
        if stat == "none":
            return 0
        return (self.__getattribute__(stat) - 10) // 2

    def dc(self, stat: str):
        return self.mod(stat) + self.prof + 8

    def add_minion(self, minion):
        self.minions.append(minion)

    def remove_minion(self, minion):
        self.minions.remove(minion)

    def add_effect(self, effect: str):
        self.effects.add(effect)

    def remove_effect(self, effect: str):
        if effect in self.effects:
            self.effects.remove(effect)

    def has_effect(self, effect: str):
        return effect in self.effects

    def use_bonus(self, source: str):
        if not self.used_bonus:
            log.record(f"Bonus ({source})", 1)
            self.used_bonus = True
            return True
        return False

    # =============================
    #       LIFECYCLE EVENTS
    # =============================

    def begin_turn(self, target: Target):
        log.record("Turn", 1)
        self.actions = 1
        self.used_bonus = False
        for feat in self.feats_for_event("begin_turn"):
            feat.begin_turn(target)

    def end_turn(self, target: Target):
        for feat in self.feats_for_event("end_turn"):
            feat.end_turn(target)
        if not self.used_bonus:
            log.record(f"Bonus (None)", 1)
        log.output(lambda: "")

    def turn(self, target: Target):
        self.begin_turn(target)
        self.before_action(target)
        while self.actions > 0:
            self.action(target)
            self.actions -= 1
        self.after_action(target)
        self.end_turn(target)
        for minion in self.minions:
            minion.turn(target)

    def before_action(self, target: Target):
        for feat in self.feats_for_event("before_action"):
            feat.before_action(target)

    def action(self, target: Target):
        for feat in self.feats_for_event("action"):
            feat.action(target)

    def after_action(self, target: Target):
        for feat in self.feats_for_event("after_action"):
            feat.after_action(target)

    def short_rest(self):
        self.effects = set()
        for feat in self.feats_for_event("short_rest"):
            feat.short_rest()

    def long_rest(self):
        self.reset_spell_slots()
        self.short_rest()
        for feat in self.feats_for_event("long_rest"):
            feat.long_rest()

    def enemy_turn(self, target: Target):
        for feat in self.feats_for_event("enemy_turn"):
            feat.enemy_turn(target)

    # ============================
    #      WEAPON ATTACKS
    # ============================

    def attack(
        self,
        target: Target,
        weapon: Weapon,
        tags: List[str] = [],
    ):
        args = AttackArgs(
            character=self,
            target=target,
            weapon=weapon,
            tags=tags,
        )
        log.record(f"Attack:{args.weapon.name}", 1)
        self.before_attack()
        if weapon.to_hit:
            to_hit = weapon.to_hit()
        else:
            to_hit = self.prof + self.mod(args.weapon.mod) + args.weapon.bonus
        result = self.roll_attack(attack=args, to_hit=to_hit)
        roll = result.roll()
        crit = False
        if roll >= args.weapon.min_crit:
            crit = True
        roll_total = roll + to_hit + result.situational_bonus
        log.output(lambda: f"{args.weapon.name} total {roll_total} vs {args.target.ac}")
        if roll_total >= args.target.ac:
            self.hit(attack=args, crit=crit, roll=roll)
        else:
            self.miss(attack=args)

    def before_attack(self):
        for feat in self.feats_for_event("before_attack"):
            feat.before_attack()

    def roll_attack(self, attack: AttackArgs, to_hit: int):
        args = AttackRollArgs(attack=attack, to_hit=to_hit)
        if attack.target.stunned:
            args.adv = True
        if attack.target.prone:
            if args.attack.weapon.ranged:
                args.disadv = True
            else:
                args.adv = True
        if attack.target.semistunned:
            args.adv = True
            args.attack.target.semistunned = False
        for feat in self.feats_for_event("roll_attack"):
            feat.roll_attack(args)
        return args

    def hit(
        self,
        attack: AttackArgs,
        crit: bool = False,
        roll: int = 0,
    ):
        args = HitArgs(attack=attack, crit=crit, roll=roll)
        for feat in self.feats_for_event("hit"):
            feat.hit(args)
        log.output(lambda: str(args._dmg))
        for key in args._dmg:
            attack.target.damage_source(key, args.dmg_multiplier * args._dmg[key])

    def miss(self, attack: AttackArgs):
        args = MissArgs(attack)
        for feat in self.feats_for_event("miss"):
            feat.miss(args)

    # ==================================
    #         SPELLCASTING
    # ==================================

    def reset_spell_slots(self):
        self.slots = spell_slots(self.level, half=self.spellcaster is Spellcaster.HALF)

    def spell_dc(self):
        return 8 + self.mod(self.spell_mod) + self.prof

    def highest_slot(self, max: int = 9) -> int:
        return highest_spell_slot(self.slots, max=max)

    def lowest_slot(self, min: int = 1) -> int:
        return lowest_spell_slot(self.slots, min=min)

    def cast(self, spell: Spell, target: Target = None):
        if spell.slot > 0:
            self.slots[spell.slot] -= 1
        if spell.concentration:
            self.set_concentration(spell)
        spell.cast(self, target)

    def set_concentration(self, spell: Spell):
        if self.concentration:
            self.concentration.end(self)
        self.concentration = spell

    def concentrating_on(self, name: str) -> bool:
        return self.concentration is not None and self.concentration.name is name

    def is_concentrating(self) -> bool:
        return self.concentration is not None

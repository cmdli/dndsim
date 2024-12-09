from util.util import prof_bonus, roll_dice
from sim.feat import Feat
from sim.feats import Vex, Feat, Topple, Graze
from sim.target import Target
from sim.weapons import Weapon
from sim.events import AttackRollArgs, AttackArgs, AttackResultArgs
from sim.event_loop import EventLoop
from util.log import log
from typing import Callable, Any, Dict, List, Tuple, Optional, Set
from sim.spellcasting import Spellcasting, Spellcaster
from sim.attack import WeaponAttack, SpellAttack
import sim.events
import math
import sim.attack
import sim.spells
import sim.weapons

STATS = ["str", "dex", "con", "int", "wis", "cha"]
DEFAULT_STAT_MAX = 20


class Character:
    def init(
        self,
        level: int,
        stats: List[int],
        base_feats: Optional[List[Feat]] = None,
        spellcaster: Spellcaster = Spellcaster.NONE,
        spell_mod: str = "none",
    ):
        base_feats = base_feats or []
        self.level = level
        self.prof = prof_bonus(level)
        self.str = stats[0]
        self.dex = stats[1]
        self.con = stats[2]
        self.int = stats[3]
        self.wis = stats[4]
        self.cha = stats[5]
        self.stat_max = {stat: DEFAULT_STAT_MAX for stat in STATS}
        self.minions: List[Character] = []
        self.events = EventLoop()
        self.effects: Set[str] = set()
        self.spells = Spellcasting(self, spell_mod, [(spellcaster, level)])
        self.masteries: List[str] = []
        self.used_bonus = False
        self.feats: Dict[str, Feat] = dict()
        for feat in [Vex(), Topple(), Graze()]:
            self.add_feat(feat)
        for feat in base_feats:
            self.add_feat(feat)

    def add_feat(self, feat: Feat):
        feat.apply(self)
        self.feats[feat.name()] = feat
        self.events.add(feat, feat.events())

    def has_feat(self, name: str):
        return name in self.feats

    def feat(self, name: str):
        return self.feats[name]

    def mod(self, stat: str):
        if stat == "none":
            return 0
        return (self.__getattribute__(stat) - 10) // 2

    def increase_stat_max(self, stat: str, amount: int):
        self.stat_max[stat] += amount

    def increase_stat(self, stat: str, amount: int):
        new_val = getattr(self, stat) + amount
        if new_val > self.stat_max[stat]:
            new_val = self.stat_max[stat]
        setattr(self, stat, new_val)

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
        self.events.emit("begin_turn", target)

    def end_turn(self, target: Target):
        self.events.emit("end_turn", target)
        if not self.used_bonus:
            log.record(f"Bonus (None)", 1)
        log.output(lambda: "")

    def turn(self, target: Target):
        self.begin_turn(target)
        self.events.emit("before_action", target)
        while self.actions > 0:
            self.events.emit("action", target)
            self.actions -= 1
        self.events.emit("after_action", target)
        self.end_turn(target)
        for minion in self.minions:
            minion.turn(target)

    def short_rest(self):
        self.effects = set()
        self.events.emit("short_rest")

    def long_rest(self):
        self.spells.reset()
        self.short_rest()
        self.events.emit("long_rest")

    def enemy_turn(self, target: Target):
        self.events.emit("enemy_turn", target)

    # ============================
    #      WEAPON ATTACKS
    # ============================

    def add_masteries(self, masteries: List[str]):
        self.masteries.extend(masteries)

    def has_mastery(self, mastery: str) -> bool:
        return mastery in self.masteries

    def weapon_attack(
        self,
        target: Target,
        weapon: Weapon,
        tags: Optional[List[str]] = None,
    ):
        attack = WeaponAttack(weapon)
        self.attack(target=target, attack=attack, weapon=weapon, tags=tags)

    def spell_attack(
        self,
        target: Target,
        spell: "sim.spells.Spell",
        damage: Optional["sim.attack.DamageRoll"] = None,
        callback: Optional["sim.events.AttackResultCallback"] = None,
        is_ranged: bool = False,
    ):
        attack = SpellAttack(
            spell,
            callback=callback,
            is_ranged=is_ranged,
            damage=damage,
        )
        self.attack(target=target, attack=attack, spell=spell)

    def attack(
        self,
        target: Target,
        attack: "sim.attack.Attack",
        weapon: Optional["sim.weapons.Weapon"] = None,
        spell: Optional["sim.spells.Spell"] = None,
        tags: Optional[List[str]] = None,
    ):
        args = AttackArgs(
            target=target, attack=attack, weapon=weapon, spell=spell, tags=tags
        )
        log.record(f"Attack:{args.attack.name}", 1)
        self.events.emit("before_attack")
        to_hit = args.attack.to_hit(self)
        roll_result = self.attack_roll(attack=args, to_hit=to_hit)
        roll = roll_result.roll()
        crit = roll >= args.attack.min_crit()
        roll_total = roll + to_hit + roll_result.situational_bonus
        hit = roll_total >= args.target.ac
        result = AttackResultArgs(attack=args, hit=hit, crit=crit, roll=roll)
        if hit:
            log.record(f"Hit ({args.attack.name})", 1)
        else:
            log.record(f"Miss ({args.attack.name})", 1)
        if crit:
            log.record(f"Crit ({args.attack.name})", 1)
        args.attack.attack_result(result, self)
        self.events.emit("attack_result", result)
        for key in result.damage_sources():
            dice = result._dice[key]
            if crit:
                dice = 2 * dice
            self.do_damage(
                target=args.target,
                source=key,
                dice=dice,
                flat_dmg=result._flat_dmg[key],
                attack=args,
                spell=args.spell,
                multiplier=result.dmg_multiplier,
            )

    def attack_roll(self, attack: AttackArgs, to_hit: int) -> AttackRollArgs:
        target = attack.target
        args = AttackRollArgs(attack=attack, to_hit=to_hit)
        if target.stunned:
            args.adv = True
        if target.prone:
            if attack.attack.is_ranged():
                args.disadv = True
            else:
                args.adv = True
        if target.semistunned:
            args.adv = True
            target.semistunned = False
        self.events.emit("attack_roll", args)
        return args

    def do_damage(
        self,
        target: Target,
        source: str,
        dice: List[int],
        flat_dmg: int = 0,
        attack: Optional["sim.events.AttackArgs"] = None,
        spell: Optional["sim.spells.Spell"] = None,
        multiplier: float = 1.0,
    ):
        args = sim.events.DamageRollArgs(
            target=target,
            dice=dice,
            flat_dmg=flat_dmg,
            attack=attack,
            spell=spell,
        )
        self.events.emit("damage_roll", args)
        target.damage_source(source, math.floor(args.damage_total() * multiplier))

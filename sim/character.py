from util.util import prof_bonus, roll_dice
from sim.feat import Feat
from sim.feats import Vex, Feat, Topple, Graze
from sim.target import Target
from sim.weapons import Weapon
from sim.events import AttackRollArgs, AttackArgs, WeaponRollArgs, AttackResultArgs
from sim.event_loop import EventLoop
from util.log import log
from typing import List
from typing import Callable, Any, Dict
from sim.spellcasting import Spellcasting, Spellcaster

STATS = ["str", "dex", "con", "int", "wis", "cha"]
DEFAULT_STAT_MAX = 20


class Character:
    def init(
        self,
        level=None,
        stats=None,
        base_feats: List[Feat] = None,
        spellcaster: Spellcaster = Spellcaster.NONE,
        spell_mod: str = None,
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
        self.effects = set()
        self.spells = Spellcasting(self, spell_mod, [(spellcaster, level)])
        self.masteries = []
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

    def attack(
        self,
        target: Target,
        weapon: Weapon,
        tags: List[str] = None,
    ):
        if tags is None:
            tags = []
        args = AttackArgs(
            character=self,
            target=target,
            weapon=weapon,
            tags=tags,
            mod=weapon.mod(self),
        )
        log.record(f"Attack:{args.weapon.name}", 1)
        self.events.emit("before_attack")
        to_hit = weapon.to_hit(self)
        result = self.roll_attack(attack=args, to_hit=to_hit)
        roll = result.roll()
        crit = roll >= args.weapon.min_crit
        roll_total = roll + to_hit + result.situational_bonus
        log.output(lambda: f"{args.weapon.name} total {roll_total} vs {args.target.ac}")
        hit = roll_total >= args.target.ac
        self.attack_result(hit=hit, attack=args, crit=crit, roll=roll)

    def roll_attack(self, attack: AttackArgs, to_hit: int) -> AttackRollArgs:
        args = AttackRollArgs(attack=attack, to_hit=to_hit)
        if attack.target.stunned:
            args.adv = True
        if attack.target.prone:
            if args.attack.weapon.has_tag("ranged"):
                args.disadv = True
            else:
                args.adv = True
        if attack.target.semistunned:
            args.adv = True
            args.attack.target.semistunned = False
        self.events.emit("roll_attack", args)
        return args

    def weapon_roll(self, weapon: Weapon, crit: bool = False):
        rolls = weapon.rolls(crit=crit)
        args = WeaponRollArgs(weapon=weapon, rolls=rolls, crit=crit)
        self.events.emit("weapon_roll", args)
        return sum(args.rolls)

    def attack_result(
        self,
        hit: bool,
        attack: AttackArgs,
        crit: bool = False,
        roll: int = 0,
    ):
        args = AttackResultArgs(hit=hit, attack=attack, crit=crit, roll=roll)
        if hit:
            log.record(f"Hit:{attack.weapon.name}", 1)
        else:
            log.record(f"Miss:{attack.weapon.name}", 1)
        if crit:
            log.record(f"Crit:{attack.weapon.name}", 1)
        attack.weapon.attack_result(args)
        self.events.emit("attack_result", args)
        for key in args._dice:
            roll = 0
            for die in args._dice[key]:
                roll += roll_dice(2 if crit else 1, die)
            attack.target.damage_source(key, args.dmg_multiplier * roll)
        for key in args._flat_dmg:
            attack.target.damage_source(key, args.dmg_multiplier * args._flat_dmg[key])

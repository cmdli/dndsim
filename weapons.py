from util import roll_dice


class Weapon:
    def __init__(
        self,
        name=None,
        num_dice=0,
        die=6,
        mod=None,
        bonus=0,
        graze=False,
        vex=False,
        min_crit=20,
        ranged=False,
        topple=False,
        base=0,
        heavy=False,
        damage_type="unknown",
        to_hit=None,
    ) -> None:
        self.name = name
        self.num_dice = num_dice
        self.die = die
        self.mod = mod
        self.bonus = bonus
        self.graze = graze
        self.vex = vex
        self.min_crit = min_crit
        self.ranged = ranged
        self.topple = topple
        self.base = base
        self.heavy = heavy
        self.damage_type = damage_type
        self.to_hit = to_hit

    def damage(self, crit: bool = False, max_reroll: int = None):
        dmg = roll_dice(self.num_dice, self.die, max_reroll=max_reroll)
        if crit:
            dmg += roll_dice(self.num_dice, self.die, max_reroll=max_reroll)
        return dmg

    def rolls(self, crit: bool = False):
        num_dice = self.num_dice
        if crit:
            num_dice *= 2
        return [roll_dice(1, self.die) for _ in range(num_dice)]


class Glaive(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Glaive",
            num_dice=1,
            die=10,
            mod="str",
            graze=True,
            heavy=True,
            damage_type="slashing",
            **kwargs,
        )


class GlaiveButt(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="GlaiveButt",
            num_dice=1,
            die=4,
            mod="str",
            graze=True,
            heavy=True,
            damage_type="bludgeoning",
            **kwargs,
        )


class Greatsword(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Greatsword",
            num_dice=2,
            die=6,
            mod="str",
            graze=True,
            heavy=True,
            damage_type="slashing",
            **kwargs,
        )


class Shortsword(Weapon):
    def __init__(self, mod="dex", name="Shortsword", **kwargs):
        super().__init__(
            name=name,
            num_dice=1,
            die=6,
            mod=mod,
            vex=True,
            damage_type="piercing",
            **kwargs,
        )


class Rapier(Weapon):
    def __init__(self, mod="dex", name="Rapier", **kwargs):
        super().__init__(
            name=name,
            num_dice=1,
            die=8,
            mod=mod,
            vex=True,
            damage_type="piercing",
            **kwargs,
        )


class Scimitar(Weapon):
    def __init__(self, mod="dex", **kwargs):
        super().__init__(
            name="Scimitar",
            num_dice=1,
            die=6,
            mod=mod,
            damage_type="slashing",
            **kwargs,
        )


class Maul(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="Maul",
            num_dice=2,
            die=6,
            mod="str",
            topple=True,
            heavy=True,
            damage_type="bludgeoning",
            **kwargs,
        )


class Quarterstaff(Weapon):
    def __init__(self, mod="str", **kwargs):
        super().__init__(
            name="Quarterstaff",
            num_dice=1,
            die=8,
            mod=mod,
            damage_type="bludgeoning",
            **kwargs,
        )


class HandCrossbow(Weapon):
    def __init__(self, **kwargs):
        super().__init__(
            name="HandCrossbow",
            num_dice=1,
            die=6,
            mod="dex",
            vex=True,
            ranged=True,
            damage_type="piercing",
            **kwargs,
        )


class Dagger(Weapon):
    def __init__(self, mod="dex", **kwargs):
        super().__init__(
            name="Dagger", num_dice=1, die=4, mod=mod, damage_type="piercing", **kwargs
        )

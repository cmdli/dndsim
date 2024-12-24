import sim.feat


class Archery(sim.feat.Feat):
    def attack_roll(self, args):
        weapon = args.attack.weapon
        if weapon and weapon.has_tag("ranged"):
            args.situational_bonus += 2


class TwoWeaponFighting(sim.feat.Feat):
    def attack_roll(self, args):
        if args.attack.has_tag("light"):
            args.attack.remove_tag("light")


class GreatWeaponFighting(sim.feat.Feat):
    def damage_roll(self, args):
        weapon = args.attack.weapon if args.attack and args.attack.weapon else None
        if weapon and weapon.has_tag("twohanded"):
            for i in range(len(args.damage.rolls)):
                if args.damage.rolls[i] == 1 or args.damage.rolls[i] == 2:
                    args.damage.rolls[i] = 3

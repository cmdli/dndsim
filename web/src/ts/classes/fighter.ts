import { GreatWeaponFighting } from "../feats/fightingStyle/GreatWeaponFighting"
import { WeaponMasteries } from "../feats/WeaponMasteries"
import { Character } from "../sim/Character"
import { ClassLevel } from "../sim/coreFeats/ClassLevel"
import { ActionEvent } from "../sim/events/ActionEvent"
import { Feat } from "../sim/Feat"
import { WeaponMastery } from "../sim/types"
import { Weapon } from "../sim/Weapon"

class ActionSurge extends Feat {
    num: number
    max: number

    constructor(max: number) {
        super()
        this.num = max
        this.max = max
    }

    apply(character: Character): void {
        character.events.on("short_rest", () => {
            this.num = this.max
        })
        character.events.on("before_action", () => {
            if (this.num > 0) {
                character.actions += 1
                this.num -= 1
            }
        })
    }
}

class StudiedAttacks extends Feat {
    enabled: boolean = false

    apply(character: Character): void {
        character.events.on("attack_roll", (data) => {
            if (this.enabled) {
                data.adv = true
                this.enabled = false
            }
        })
        character.events.on("attack_result", (data) => {
            if (!data.hit) {
                this.enabled = true
            }
        })
    }
}

export function fighterFeats(
    level: number,
    masteries: WeaponMastery[],
    fightingStyle: Feat
): Feat[] {
    const feats: Feat[] = []
    if (level >= 1) {
        feats.push(new ClassLevel("Fighter", level))
        feats.push(new WeaponMasteries(masteries))
        feats.push(fightingStyle)
    }
    if (level >= 2) {
        feats.push(new ActionSurge(level >= 17 ? 2 : 1))
    }
    if (level >= 13) {
        feats.push(new StudiedAttacks())
    }
    return feats
}

class FighterAction extends Feat {
    numAttacks: number
    weapon: Weapon
    toppleWeapon?: Weapon
    nickWeapon?: Weapon

    constructor(args: {
        numAttacks: number
        weapon: Weapon
        toppleWeapon?: Weapon
        nickWeapon?: Weapon
    }) {
        super()
        this.numAttacks = args.numAttacks
        this.weapon = args.weapon
        this.toppleWeapon = args.toppleWeapon
        this.nickWeapon = args.nickWeapon
    }

    apply(character: Character): void {
        character.events.on("action", (data) => this.action(data))
    }

    action(data: ActionEvent): void {
        for (let i = 0; i < this.numAttacks; i++) {
            let weapon = this.weapon
            if (
                this.toppleWeapon &&
                !data.target.prone &&
                i < this.numAttacks - 1
            ) {
                weapon = this.toppleWeapon
            }
            this.character?.weaponAttack({
                target: data.target,
                weapon,
                tags: ["main_action"],
            })
        }
    }
}

export function createFighter(level: number): Character {
    const character = new Character()
    const feats = fighterFeats(level, [], new GreatWeaponFighting())
    feats.forEach((feat) => character.addFeat(feat))
    return character
}

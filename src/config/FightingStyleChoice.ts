import { Character } from "../sim/Character"
import { Archery } from "../feats/fightingStyle/Archery"
import { Choice, StaticOption } from "./config"
import { BlindFighting } from "../feats/fightingStyle/BlindFighting"
import { Defense } from "../feats/fightingStyle/Defense"
import { GreatWeaponFighting } from "../feats/fightingStyle/GreatWeaponFighting"
import { Interception } from "../feats/fightingStyle/Interception"
import { Dueling } from "../feats/fightingStyle/Dueling"
import { Protection } from "../feats/fightingStyle/Protection"
import { ThrownWeaponFighting } from "../feats/fightingStyle/ThrownWeaponFighting"
import { TwoWeaponFighting } from "../feats/fightingStyle/TwoWeaponFighting"
import { UnarmedFighting } from "../feats/fightingStyle/UnarmedFighting"

const FIGHTING_STYLES = {
    Archery: {
        id: "Archery",
        name: "Archery",
        feat: () => new Archery(),
    },
    BlindFighting: {
        id: "BlindFighting",
        name: "Blind Fighting",
        feat: () => new BlindFighting(),
    },
    Defense: {
        id: "Defense",
        name: "Defense",
        feat: () => new Defense(),
    },
    Dueling: {
        id: "Dueling",
        name: "Dueling",
        feat: () => new Dueling(),
    },
    GreatWeaponFighting: {
        id: "GreatWeaponFighting",
        name: "Great Weapon Fighting",
        feat: () => new GreatWeaponFighting(),
    },
    Interception: {
        id: "Interception",
        name: "Interception",
        feat: () => new Interception(),
    },
    Protection: {
        id: "Protection",
        name: "Protection",
        feat: () => new Protection(),
    },
    ThrownWeaponFighting: {
        id: "ThrownWeaponFighting",
        name: "Thrown Weapon Fighting",
        feat: () => new ThrownWeaponFighting(),
    },
    TwoWeaponFighting: {
        id: "TwoWeaponFighting",
        name: "Two Weapon Fighting",
        feat: () => new TwoWeaponFighting(),
    },
    UnarmedFighting: {
        id: "UnarmedFighting",
        name: "Unarmed Fighting",
        feat: () => new UnarmedFighting(),
    },
} as const

type FightingStyleName = keyof typeof FIGHTING_STYLES

export class FightingStyleChoice implements Choice {
    options(character: Character) {
        return Object.values(FIGHTING_STYLES).map(
            (config) => new StaticOption(config.id)
        )
    }

    apply(character: Character, option: FightingStyleName) {
        const config = FIGHTING_STYLES[option]
        character.addFeature(config.feat())
    }
}

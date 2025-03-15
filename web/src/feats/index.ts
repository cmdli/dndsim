import { IrresistibleOffense } from "./epic/IrresistibleOffense"
import { Archery } from "./fightingStyle/Archery"
import { BlindFighting } from "./fightingStyle/BlindFighting"
import { Defense } from "./fightingStyle/Defense"
import { Dueling } from "./fightingStyle/Dueling"
import { GreatWeaponFighting } from "./fightingStyle/GreatWeaponFighting"
import { Interception } from "./fightingStyle/Interception"
import { Protection } from "./fightingStyle/Protection"
import { ThrownWeaponFighting } from "./fightingStyle/ThrownWeaponFighting"
import { TwoWeaponFighting } from "./fightingStyle/TwoWeaponFighting"
import { UnarmedFighting } from "./fightingStyle/UnarmedFighting"
import { GreatWeaponMaster } from "./GreatWeaponMaster"
import { Alert } from "./origin/Alert"
import { Crafter } from "./origin/Crafter"
import { Healer } from "./origin/Healer"
import { Lucky } from "./origin/Lucky"
import { MagicInitiate } from "./origin/MagicInitiate"
import { Musician } from "./origin/Musician"
import { SavageAttacker } from "./origin/SavageAttacker"
import { Skilled } from "./origin/Skilled"
import { TavernBrawler } from "./origin/TavernBrawler"
import { Tough } from "./origin/Tough"
import { AbilityScoreImprovement } from "./shared/AbilityScoreImprovement"

const epicBoons = {
    IrresistibleOffense,
    GreatWeaponFighting,
}

const fightingStyles = {
    Archery,
    BlindFighting,
    Defense,
    Dueling,
    GreatWeaponFighting,
    Interception,
    Protection,
    ThrownWeaponFighting,
    TwoWeaponFighting,
    UnarmedFighting,
}

const originFeats = {
    Alert,
    Crafter,
    Healer,
    Lucky,
    MagicInitiate,
    Musician,
    SavageAttacker,
    Skilled,
    TavernBrawler,
    Tough,
}

export {
    GreatWeaponMaster,
    AbilityScoreImprovement,
    epicBoons,
    fightingStyles,
    originFeats,
}

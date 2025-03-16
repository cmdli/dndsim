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
import { GreatWeaponMaster } from "./general/GreatWeaponMaster"
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
import { AbilityScoreImprovement } from "./general/AbilityScoreImprovement"
import { Actor } from "./general/Actor"
import { Athlete } from "./general/Athlete"
import { Charger } from "./general/Charger"
import { Chef } from "./general/Chef"
import { CrossbowExpert } from "./general/CrossbowExpert"
import { Crusher } from "./general/Crusher"
import { DefensiveDuelist } from "./general/DefensiveDuelist"
import { DualWielder } from "./general/DualWielder"
import { Durable } from "./general/Durable"
import { ElementalAdept } from "./general/ElementalAdept"
import { FeyTouched } from "./general/FeyTouched"
import { Grappler } from "./general/Grappler"
import { HeavilyArmored } from "./general/HeavilyArmored"
import { HeavyArmorMaster } from "./general/HeavyArmorMaster"
import { InspiringLeader } from "./general/InspiringLeader"
import { KeenMind } from "./general/KeenMind"
import { LightlyArmored } from "./general/LightlyArmored"
import { MageSlayer } from "./general/MageSlayer"
import { MartialWeaponTraining } from "./general/MartialWeaponTraining"
import { MediumArmorMaster } from "./general/MediumArmorMaster"
import { ModeratelyArmored } from "./general/ModeratelyArmored"
import { MountedCombatant } from "./general/MountedCombatant_TODO"
import { Observant } from "./general/Observant"
import { Piercer } from "./general/Piercer"
import { Poisoner } from "./general/Poisoner"
import { PolearmMaster } from "./general/PolearmMaster_TODO"
import { Resilient } from "./general/Resilient"
import { RitualCaster } from "./general/RitualCaster"
import { Sentinel } from "./general/Sentinel"
import { ShadowTouched } from "./general/ShadowTouched"
import { Sharpshooter } from "./general/Sharpshooter"
import { ShieldMaster } from "./general/ShieldMaster"
import { SkillExpert } from "./general/SkillExpert"
import { Skulker } from "./general/Skulker"
import { Slasher } from "./general/Slasher"
import { Speedy } from "./general/Speedy"
import { SpellSniper } from "./general/SpellSniper"
import { Telekinetic } from "./general/Telekinetic"
import { Telepathic } from "./general/Telepathic"
import { WarCaster } from "./general/WarCaster"
import { WeaponMaster } from "./general/WeaponMaster"

const epicBoons = {
    IrresistibleOffense,
    GreatWeaponFighting,
}

const fightingStyle = {
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

const origin = {
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

const general = {
    AbilityScoreImprovement,
    Actor,
    Athlete,
    Charger,
    Chef,
    CrossbowExpert,
    Crusher,
    DefensiveDuelist,
    DualWielder,
    Durable,
    ElementalAdept,
    FeyTouched,
    Grappler,
    GreatWeaponMaster,
    HeavilyArmored,
    HeavyArmorMaster,
    InspiringLeader,
    KeenMind,
    LightlyArmored,
    MageSlayer,
    MartialWeaponTraining,
    MediumArmorMaster,
    ModeratelyArmored,
    MountedCombatant,
    Observant,
    Piercer,
    Poisoner,
    PolearmMaster,
    Resilient,
    RitualCaster,
    Sentinel,
    ShadowTouched,
    Sharpshooter,
    ShieldMaster,
    SkillExpert,
    Skulker,
    Slasher,
    Speedy,
    SpellSniper,
    Telekinetic,
    Telepathic,
    WarCaster,
    WeaponMaster,
}

export { general, epicBoons, fightingStyle, origin }

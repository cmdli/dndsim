// Types for basic D&D properties
type Ability = 'strength' | 'dexterity' | 'constitution' | 'intelligence' | 'wisdom' | 'charisma';
type SkillProficiency = 'none' | 'proficient' | 'expert';

// Character class configuration
interface ClassLevel {
    class: string;
    level: number;
    subclass?: string;
    classFeatures: string[];
}

// Feat configuration
interface Feat {
    name: string;
    prerequisites?: {
        level?: number;
        abilities?: Partial<Record<Ability, number>>;
        race?: string[];
        class?: string[];
    };
    benefits: string[];
}

// Skill configuration
interface Skill {
    name: string;
    ability: Ability;
    proficiency: SkillProficiency;
}

// Main character configuration interface
interface DndCharacterConfig {
    // Basic character info
    name: string;
    race: string;
    background: string;
    alignment?: string;
    
    // Class configuration
    classes: ClassLevel[];
    
    // Ability scores
    abilityScores: Record<Ability, number>;
    
    // Skills and proficiencies
    skills: Skill[];
    
    // Feats
    feats: Feat[];
    
    // Equipment
    equipment: {
        armor?: string;
        weapons: string[];
        items: string[];
        magicItems: string[];
    };
}

// Example usage:
const exampleCharacter: DndCharacterConfig = {
    name: "Thorin Ironforge",
    race: "Mountain Dwarf",
    background: "Soldier",
    alignment: "Lawful Good",
    
    classes: [{
        class: "Fighter",
        level: 5,
        subclass: "Battle Master",
        classFeatures: ["Second Wind", "Action Surge", "Combat Superiority"]
    }],
    
    abilityScores: {
        strength: 16,
        dexterity: 12,
        constitution: 16,
        intelligence: 10,
        wisdom: 13,
        charisma: 8
    },
    
    skills: [
        {
            name: "Athletics",
            ability: "strength",
            proficiency: "proficient"
        },
        {
            name: "Intimidation",
            ability: "charisma",
            proficiency: "proficient"
        }
    ],
    
    feats: [{
        name: "Heavy Armor Master",
        prerequisites: {
            abilities: { strength: 15 },
        },
        benefits: [
            "Reduce non-magical bludgeoning, piercing, and slashing damage by 3"
        ]
    }],
    
    equipment: {
        armor: "Plate Armor",
        weapons: ["Battleaxe", "Warhammer"],
        items: ["Backpack", "Bedroll", "Rations (10 days)"],
        magicItems: []
    }
};

export type {
    DndCharacterConfig,
    ClassLevel,
    Feat,
    Skill,
    Ability,
    SkillProficiency
}; 
import random
from typing import Dict, Any

class CharacterSystem:
    """Handles character creation, progression, and management"""
    
    def __init__(self):
        self.character_classes = self._initialize_classes()
    
    def _initialize_classes(self) -> Dict[str, Dict[str, Any]]:
        """Initialize all available character classes"""
        return {
            'swordsman': {
                'icon': '⚔️',
                'description': 'Master of blade combat with high attack and defense',
                'base_stats': {
                    'strength': 18,
                    'agility': 12,
                    'intelligence': 10,
                    'defense': 16,
                    'magic_power': 8,
                    'max_hp': 120
                },
                'abilities': ['Sword Mastery', 'Heavy Strike', 'Parry'],
                'lore': 'The Swordsman has trained for years in the art of blade combat, '
                       'becoming a formidable warrior capable of facing the fiercest beasts.'
            },
            'sniper': {
                'icon': '🎯',
                'description': 'Long-range specialist with deadly accuracy',
                'base_stats': {
                    'strength': 12,
                    'agility': 20,
                    'intelligence': 14,
                    'defense': 10,
                    'magic_power': 8,
                    'max_hp': 90
                },
                'abilities': ['Eagle Eye', 'Piercing Shot', 'Stealth'],
                'lore': 'The Sniper can eliminate threats from impossible distances, '
                       'using precision and patience to bring down even the largest creatures.'
            },
            'magician': {
                'icon': '🔮',
                'description': 'Wielder of arcane magic with devastating spells',
                'base_stats': {
                    'strength': 8,
                    'agility': 10,
                    'intelligence': 20,
                    'defense': 8,
                    'magic_power': 18,
                    'max_hp': 80
                },
                'abilities': ['Fireball', 'Magic Shield', 'Arcane Blast'],
                'lore': 'The Magician harnesses the raw power of magic itself, '
                       'capable of unleashing devastating spells against ancient foes.'
            },
            'gunman': {
                'icon': '🔫',
                'description': 'Firearms expert with rapid-fire capabilities',
                'base_stats': {
                    'strength': 14,
                    'agility': 16,
                    'intelligence': 12,
                    'defense': 12,
                    'magic_power': 6,
                    'max_hp': 100
                },
                'abilities': ['Rapid Fire', 'Reload', 'Precise Aim'],
                'lore': 'The Gunman brings modern firepower to ancient battles, '
                       'using advanced weapons to level the playing field.'
            },
            'archer': {
                'icon': '🏹',
                'description': 'Swift bow user with nature-based abilities',
                'base_stats': {
                    'strength': 12,
                    'agility': 18,
                    'intelligence': 12,
                    'defense': 10,
                    'magic_power': 10,
                    'max_hp': 95
                },
                'abilities': ['Multi-Shot', 'Nature\'s Blessing', 'Track'],
                'lore': 'The Archer moves like the wind through ancient forests, '
                       'using bow and nature magic to hunt the most elusive prey.'
            },
            'warrior': {
                'icon': '🛡️',
                'description': 'Balanced fighter with strong defensive capabilities',
                'base_stats': {
                    'strength': 16,
                    'agility': 12,
                    'intelligence': 10,
                    'defense': 18,
                    'magic_power': 8,
                    'max_hp': 130
                },
                'abilities': ['Shield Bash', 'Taunt', 'Endurance'],
                'lore': 'The Warrior stands as an unbreakable wall against the darkness, '
                       'protecting allies and striking down enemies with equal skill.'
            },
            'hunter': {
                'icon': '🐺',
                'description': 'Beast tracker with survival skills and traps',
                'base_stats': {
                    'strength': 14,
                    'agility': 16,
                    'intelligence': 14,
                    'defense': 12,
                    'magic_power': 8,
                    'max_hp': 110
                },
                'abilities': ['Beast Lore', 'Trap Setting', 'Camouflage'],
                'lore': 'The Hunter knows the ways of all creatures, using this knowledge '
                       'to track and defeat even the most cunning ancient beasts.'
            },
            'assassin': {
                'icon': '🗡️',
                'description': 'Stealthy killer with critical strike abilities',
                'base_stats': {
                    'strength': 12,
                    'agility': 20,
                    'intelligence': 12,
                    'defense': 8,
                    'magic_power': 10,
                    'max_hp': 85
                },
                'abilities': ['Stealth Strike', 'Poison Blade', 'Shadow Step'],
                'lore': 'The Assassin strikes from the shadows with lethal precision, '
                       'eliminating threats before they know danger approaches.'
            },
            'hitman': {
                'icon': '💀',
                'description': 'Professional eliminator with tactical expertise',
                'base_stats': {
                    'strength': 14,
                    'agility': 16,
                    'intelligence': 16,
                    'defense': 10,
                    'magic_power': 6,
                    'max_hp': 95
                },
                'abilities': ['Tactical Strike', 'Equipment Mastery', 'Cold Blood'],
                'lore': 'The Hitman approaches each hunt as a professional contract, '
                       'using advanced tactics and equipment to ensure success.'
            }
        }
    
    def get_available_classes(self) -> Dict[str, Dict[str, Any]]:
        """Get all available character classes"""
        return self.character_classes
    
    def create_character(self, name: str, character_class: str) -> Dict[str, Any]:
        """Create a new character with the specified class"""
        if character_class not in self.character_classes:
            raise ValueError(f"Invalid character class: {character_class}")
        
        class_data = self.character_classes[character_class]
        
        character = {
            'name': name,
            'class': character_class,
            'level': 1,
            'experience': 0,
            'experience_to_next': 100,
            'gold': 100,  # Starting gold
            'stats': class_data['base_stats'].copy(),
            'current_hp': class_data['base_stats']['max_hp'],
            'max_hp': class_data['base_stats']['max_hp'],
            'abilities': class_data['abilities'].copy(),
            'inventory': {
                'weapons': [],
                'armor': [],
                'items': [],
                'spells': []
            },
            'quests_completed': 0,
            'monsters_defeated': 0
        }
        
        return character
    
    def level_up(self, character: Dict[str, Any]) -> Dict[str, Any]:
        """Level up the character and improve stats"""
        character['level'] += 1
        character['experience'] = 0
        character['experience_to_next'] = character['level'] * 100
        
        # Stat increases based on class
        class_data = self.character_classes[character['class']]
        stat_growth = self._calculate_stat_growth(class_data)
        
        for stat, growth in stat_growth.items():
            character['stats'][stat] += growth
        
        # Increase max HP and restore to full
        hp_increase = random.randint(8, 15)
        character['stats']['max_hp'] += hp_increase
        character['max_hp'] = character['stats']['max_hp']
        character['current_hp'] = character['max_hp']
        
        return character
    
    def _calculate_stat_growth(self, class_data: Dict[str, Any]) -> Dict[str, int]:
        """Calculate stat growth for level up based on class"""
        base_stats = class_data['base_stats']
        growth = {}
        
        for stat, base_value in base_stats.items():
            if stat == 'max_hp':
                continue  # HP handled separately
            
            # Higher base stats grow more
            if base_value >= 16:
                growth[stat] = random.randint(2, 4)
            elif base_value >= 12:
                growth[stat] = random.randint(1, 3)
            else:
                growth[stat] = random.randint(1, 2)
        
        return growth
    
    def add_item(self, character: Dict[str, Any], item: Dict[str, Any]) -> bool:
        """Add an item to character's inventory"""
        item_type = item.get('type', 'items')
        
        if item_type in character['inventory']:
            character['inventory'][item_type].append(item)
            return True
        
        return False
    
    def remove_item(self, character: Dict[str, Any], item_name: str, item_type: str) -> bool:
        """Remove an item from character's inventory"""
        if item_type in character['inventory']:
            items = character['inventory'][item_type]
            for i, item in enumerate(items):
                if item.get('name') == item_name:
                    items.pop(i)
                    return True
        
        return False
    
    def calculate_damage(self, character: Dict[str, Any], ability: str = None) -> int:
        """Calculate damage dealt by character"""
        base_damage = character['stats']['strength']
        
        # Add weapon bonuses if equipped
        # This would be expanded with actual weapon system
        
        # Add ability modifiers
        if ability:
            damage_modifier = self._get_ability_damage_modifier(character['class'], ability)
            base_damage = int(base_damage * damage_modifier)
        
        # Add some randomness
        variance = random.randint(-5, 5)
        return max(1, base_damage + variance)
    
    def _get_ability_damage_modifier(self, character_class: str, ability: str) -> float:
        """Get damage modifier for specific abilities"""
        ability_modifiers = {
            'swordsman': {'Heavy Strike': 1.5, 'Sword Mastery': 1.2},
            'sniper': {'Piercing Shot': 1.8, 'Eagle Eye': 1.3},
            'magician': {'Fireball': 2.0, 'Arcane Blast': 1.7},
            'gunman': {'Rapid Fire': 1.4, 'Precise Aim': 1.6},
            'archer': {'Multi-Shot': 1.3, 'Track': 1.1},
            'warrior': {'Shield Bash': 1.2, 'Endurance': 1.0},
            'hunter': {'Beast Lore': 1.4, 'Trap Setting': 1.3},
            'assassin': {'Stealth Strike': 2.2, 'Poison Blade': 1.6},
            'hitman': {'Tactical Strike': 1.8, 'Equipment Mastery': 1.3}
        }
        
        return ability_modifiers.get(character_class, {}).get(ability, 1.0)

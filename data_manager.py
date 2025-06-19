import json
import os
from typing import Dict, Any, List, Optional

class DataManager:
    """Handles data storage and retrieval for the game"""
    
    def __init__(self):
        self.data_dir = "game_data"
        self.save_file = os.path.join(self.data_dir, "save_game.json")
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Ensure game data directory exists"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def save_game_state(self, game_state: Dict[str, Any]) -> bool:
        """Save current game state to file"""
        try:
            with open(self.save_file, 'w') as f:
                json.dump(game_state, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save game state: {e}")
            return False
    
    def load_game_state(self) -> Optional[Dict[str, Any]]:
        """Load saved game state from file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Failed to load game state: {e}")
        return None
    
    def get_monsters(self) -> List[Dict[str, Any]]:
        """Get monster data"""
        # This could be loaded from a JSON/CSV file in a real implementation
        return [
            {
                'id': 1,
                'name': 'Tyrannosaurus Rex',
                'type': 'dinosaur',
                'difficulty': 'legendary',
                'habitat': 'ancient_forest'
            },
            {
                'id': 2,
                'name': 'Woolly Mammoth',
                'type': 'mammal',
                'difficulty': 'hard',
                'habitat': 'frozen_plains'
            },
            {
                'id': 3,
                'name': 'Saber-tooth Tiger',
                'type': 'mammal',
                'difficulty': 'medium',
                'habitat': 'mountain_caves'
            }
        ]
    
    def get_items(self) -> List[Dict[str, Any]]:
        """Get item data"""
        return [
            {
                'id': 1,
                'name': 'Iron Sword',
                'type': 'weapon',
                'rarity': 'common',
                'stats': {'attack': 10}
            },
            {
                'id': 2,
                'name': 'Health Potion',
                'type': 'consumable',
                'rarity': 'common',
                'effect': {'heal': 50}
            },
            {
                'id': 3,
                'name': 'Dragon Scale Armor',
                'type': 'armor',
                'rarity': 'legendary',
                'stats': {'defense': 25}
            }
        ]
    
    def get_spells(self) -> List[Dict[str, Any]]:
        """Get spell data"""
        return [
            {
                'id': 1,
                'name': 'Fireball',
                'type': 'offensive',
                'mana_cost': 15,
                'damage': 25,
                'description': 'Launches a ball of fire at the target'
            },
            {
                'id': 2,
                'name': 'Heal',
                'type': 'healing',
                'mana_cost': 10,
                'heal_amount': 40,
                'description': 'Restores health to the caster'
            },
            {
                'id': 3,
                'name': 'Shield',
                'type': 'defensive',
                'mana_cost': 12,
                'defense_bonus': 15,
                'description': 'Creates a magical barrier'
            }
        ]
    
    def create_player_dataframe(self, players: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create player data structure for analysis"""
        if not players:
            return {}
        
        return {
            'total_players': len(players),
            'players': players,
            'avg_level': sum(p.get('level', 1) for p in players) / len(players) if players else 0
        }
    
    def get_player_statistics(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """Get statistical analysis of player performance"""
        stats = {
            'total_experience': player.get('experience', 0),
            'quests_completed': player.get('quests_completed', 0),
            'monsters_defeated': player.get('monsters_defeated', 0),
            'current_level': player.get('level', 1),
            'gold_earned': player.get('gold', 0)
        }
        
        # Calculate derived stats
        if stats['quests_completed'] > 0:
            stats['avg_experience_per_quest'] = stats['total_experience'] / stats['quests_completed']
        else:
            stats['avg_experience_per_quest'] = 0
        
        return stats
    
    def export_game_data(self, player: Dict[str, Any], story_context: List[Dict[str, Any]]) -> str:
        """Export game data to JSON string for backup/sharing"""
        import time
        export_data = {
            'player': player,
            'story_context': story_context,
            'export_timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return json.dumps(export_data, indent=2)
    
    def import_game_data(self, json_data: str) -> Optional[Dict[str, Any]]:
        """Import game data from JSON string"""
        try:
            return json.loads(json_data)
        except Exception as e:
            print(f"Failed to import game data: {e}")
            return None
    
    def clear_save_data(self) -> bool:
        """Clear all saved game data"""
        try:
            if os.path.exists(self.save_file):
                os.remove(self.save_file)
            return True
        except Exception as e:
            print(f"Failed to clear save data: {e}")
            return False

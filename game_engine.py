from character_system import CharacterSystem
from quest_system import QuestSystem
from combat_system import CombatSystem
from ai_story_generator import AIStoryGenerator
from data_manager import DataManager

class GameEngine:
    """Main game engine that coordinates all game systems"""
    
    def __init__(self):
        self.character_system = CharacterSystem()
        self.quest_system = QuestSystem()
        self.combat_system = CombatSystem()
        self.ai_story_generator = AIStoryGenerator()
        self.data_manager = DataManager()
        
        # Initialize game data
        self._initialize_game_data()
    
    def _initialize_game_data(self):
        """Initialize base game data and monsters"""
        self.monsters = self.data_manager.get_monsters()
        self.items = self.data_manager.get_items()
        self.spells = self.data_manager.get_spells()
    
    def save_game_state(self, player, quest_state, story_context):
        """Save current game state"""
        game_state = {
            'player': player,
            'quest_state': quest_state,
            'story_context': story_context
        }
        return self.data_manager.save_game_state(game_state)
    
    def load_game_state(self):
        """Load saved game state"""
        return self.data_manager.load_game_state()
    
    def get_game_stats(self):
        """Get overall game statistics"""
        return {
            'total_monsters': len(self.monsters),
            'total_items': len(self.items),
            'total_spells': len(self.spells)
        }

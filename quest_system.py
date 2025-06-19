import random
from typing import Dict, Any, List
from ai_story_generator import AIStoryGenerator

class QuestSystem:
    """Handles quest generation, management, and completion"""
    
    def __init__(self):
        self.ai_story_generator = AIStoryGenerator()
        self.quest_templates = self._initialize_quest_templates()
        self.ancient_creatures = self._initialize_ancient_creatures()
        self.quest_givers = self._initialize_quest_givers()
    
    def _initialize_quest_templates(self) -> List[Dict[str, Any]]:
        """Initialize quest templates for variety"""
        return [
            {
                'type': 'hunt',
                'title_format': 'Hunt the {creature}',
                'description_format': 'A {creature} has been spotted {location}. Eliminate this threat before it causes more damage.',
                'difficulty_modifier': 1.0
            },
            {
                'type': 'protect',
                'title_format': 'Protect {location} from {creature}',
                'description_format': 'The {creature} is threatening {location}. Defend our people and drive back this ancient menace.',
                'difficulty_modifier': 1.2
            },
            {
                'type': 'investigate',
                'title_format': 'Investigate {creature} Sightings',
                'description_format': 'Strange {creature} tracks have been found {location}. Investigate and eliminate any threats.',
                'difficulty_modifier': 0.9
            },
            {
                'type': 'urgent',
                'title_format': 'URGENT: {creature} Attack!',
                'description_format': 'A {creature} is actively attacking {location}! Respond immediately!',
                'difficulty_modifier': 1.5
            }
        ]
    
    def _initialize_ancient_creatures(self) -> List[Dict[str, Any]]:
        """Initialize ancient creatures that can be hunted"""
        return [
            {
                'name': 'Tyrannosaurus Rex',
                'description': 'The apex predator of the ancient world',
                'difficulty': 'legendary',
                'hp': 200,
                'attack': 25,
                'defense': 15,
                'special_abilities': ['Crushing Bite', 'Intimidating Roar'],
                'lore': 'The king of all predators has returned from extinction'
            },
            {
                'name': 'Woolly Mammoth',
                'description': 'Massive ancient elephant with deadly tusks',
                'difficulty': 'hard',
                'hp': 180,
                'attack': 20,
                'defense': 18,
                'special_abilities': ['Tusk Charge', 'Trumpet Call'],
                'lore': 'These giants once roamed frozen lands'
            },
            {
                'name': 'Saber-tooth Tiger',
                'description': 'Fierce predator with razor-sharp fangs',
                'difficulty': 'medium',
                'hp': 120,
                'attack': 22,
                'defense': 12,
                'special_abilities': ['Pounce', 'Saber Strike'],
                'lore': 'Swift and deadly hunter of the ice age'
            },
            {
                'name': 'Cave Bear',
                'description': 'Enormous bear from prehistoric times',
                'difficulty': 'medium',
                'hp': 140,
                'attack': 18,
                'defense': 16,
                'special_abilities': ['Claw Swipe', 'Bear Hug'],
                'lore': 'Massive bears that once ruled mountain caves'
            },
            {
                'name': 'Giant Ground Sloth',
                'description': 'Deceptively dangerous prehistoric giant',
                'difficulty': 'easy',
                'hp': 100,
                'attack': 15,
                'defense': 14,
                'special_abilities': ['Heavy Slam', 'Thick Hide'],
                'lore': 'Slow but incredibly strong ancient herbivore'
            },
            {
                'name': 'Terror Bird',
                'description': 'Flightless predatory bird of enormous size',
                'difficulty': 'medium',
                'hp': 110,
                'attack': 20,
                'defense': 10,
                'special_abilities': ['Piercing Beak', 'Swift Strike'],
                'lore': 'These giant birds were apex predators in their time'
            },
            {
                'name': 'Dire Wolf',
                'description': 'Pack hunter larger than modern wolves',
                'difficulty': 'easy',
                'hp': 80,
                'attack': 16,
                'defense': 12,
                'special_abilities': ['Pack Howl', 'Bite and Hold'],
                'lore': 'Ancestors of modern wolves, but much larger and fiercer'
            },
            {
                'name': 'Megalania',
                'description': 'Giant monitor lizard with venomous bite',
                'difficulty': 'hard',
                'hp': 160,
                'attack': 19,
                'defense': 16,
                'special_abilities': ['Venomous Bite', 'Tail Whip'],
                'lore': 'Massive lizard that dominated ancient Australia'
            }
        ]
    
    def _initialize_quest_givers(self) -> List[Dict[str, str]]:
        """Initialize NPCs who give quests"""
        return [
            {'name': 'Captain Marcus', 'title': 'Royal Guard Captain'},
            {'name': 'Elder Sarah', 'title': 'Village Elder'},
            {'name': 'Scout Tobias', 'title': 'Guild Scout'},
            {'name': 'Merchant Willem', 'title': 'Trade Master'},
            {'name': 'Priestess Elena', 'title': 'Temple Keeper'},
            {'name': 'Hunter Gareth', 'title': 'Senior Monster Hunter'},
            {'name': 'Scholar Aramis', 'title': 'Royal Historian'},
            {'name': 'Knight Commander Lyra', 'title': 'Knight Commander'}
        ]
    
    def generate_quest(self, player: Dict[str, Any], story_context: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate an AI-powered quest based on player and story context"""
        # Select quest template and creature based on player level
        template = self._select_quest_template(player)
        creature = self._select_creature_for_player(player)
        quest_giver = random.choice(self.quest_givers)
        location = self._generate_location()
        
        # Create base quest
        quest = {
            'title': template['title_format'].format(
                creature=creature['name'], 
                location=location
            ),
            'description': template['description_format'].format(
                creature=creature['name'], 
                location=location
            ),
            'type': template['type'],
            'giver': f"{quest_giver['name']}, {quest_giver['title']}",
            'target': creature,
            'location': location,
            'difficulty': creature['difficulty'],
            'reward': self._calculate_rewards(player, creature, template['difficulty_modifier'])
        }
        
        # Use AI to enhance the quest with story context
        try:
            enhanced_quest = self.ai_story_generator.enhance_quest(quest, player, story_context)
            if enhanced_quest:
                quest.update(enhanced_quest)
        except Exception as e:
            print(f"AI enhancement failed: {e}")
            # Continue with basic quest if AI fails
        
        return quest
    
    def _select_quest_template(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """Select appropriate quest template based on player"""
        # Could add logic to select based on player preferences or story
        return random.choice(self.quest_templates)
    
    def _select_creature_for_player(self, player: Dict[str, Any]) -> Dict[str, Any]:
        """Select creature appropriate for player level"""
        level = player['level']
        
        if level <= 2:
            suitable_creatures = [c for c in self.ancient_creatures if c['difficulty'] == 'easy']
        elif level <= 5:
            suitable_creatures = [c for c in self.ancient_creatures if c['difficulty'] in ['easy', 'medium']]
        elif level <= 8:
            suitable_creatures = [c for c in self.ancient_creatures if c['difficulty'] in ['medium', 'hard']]
        else:
            suitable_creatures = self.ancient_creatures  # All creatures available
        
        creature = random.choice(suitable_creatures).copy()
        
        # Scale creature stats based on player level
        level_modifier = 1 + (level - 1) * 0.1  # 10% increase per level
        creature['hp'] = int(creature['hp'] * level_modifier)
        creature['attack'] = int(creature['attack'] * level_modifier)
        creature['defense'] = int(creature['defense'] * level_modifier)
        creature['max_hp'] = creature['hp']
        creature['current_hp'] = creature['hp']
        
        return creature
    
    def _generate_location(self) -> str:
        """Generate a random location for the quest"""
        locations = [
            'near the Ancient Forest',
            'in the Forgotten Ruins',
            'at the Mountain Pass',
            'by the Mystic Lake',
            'in the Dark Caverns',
            'at the Village Outskirts',
            'near the Old Watchtower',
            'in the Haunted Valley',
            'at the Crossroads',
            'by the River Bend',
            'in the Stone Circle',
            'near the Abandoned Mine',
            'at the Merchant\'s Route',
            'in the Whispering Woods',
            'by the Crystal Falls'
        ]
        return random.choice(locations)
    
    def _calculate_rewards(self, player: Dict[str, Any], creature: Dict[str, Any], difficulty_modifier: float) -> Dict[str, Any]:
        """Calculate quest rewards based on player level and creature difficulty"""
        base_gold = 50 + (player['level'] * 25)
        base_exp = 40 + (player['level'] * 20)
        
        # Difficulty modifiers
        difficulty_multipliers = {
            'easy': 0.8,
            'medium': 1.0,
            'hard': 1.3,
            'legendary': 1.6
        }
        
        multiplier = difficulty_multipliers.get(creature['difficulty'], 1.0) * difficulty_modifier
        
        rewards = {
            'gold': int(base_gold * multiplier),
            'experience': int(base_exp * multiplier),
            'items': []
        }
        
        # Chance for item rewards
        if random.random() < 0.3:  # 30% chance for items
            rewards['items'] = self._generate_reward_items(creature)
        
        return rewards
    
    def _generate_reward_items(self, creature: Dict[str, Any]) -> List[str]:
        """Generate item rewards based on creature type"""
        possible_items = [
            f"{creature['name']} Fang",
            f"{creature['name']} Hide",
            f"{creature['name']} Claw",
            "Ancient Bone Fragment",
            "Prehistoric Essence",
            "Monster Trophy",
            "Health Potion",
            "Strength Elixir"
        ]
        
        num_items = random.randint(1, 2)
        return random.sample(possible_items, min(num_items, len(possible_items)))
    
    def complete_quest(self, quest: Dict[str, Any], player: Dict[str, Any]) -> Dict[str, Any]:
        """Complete a quest and apply rewards"""
        # Apply rewards
        player['gold'] += quest['reward']['gold']
        player['experience'] += quest['reward']['experience']
        player['quests_completed'] += 1
        player['monsters_defeated'] += 1
        
        # Add items to inventory
        for item_name in quest['reward'].get('items', []):
            item = {'name': item_name, 'type': 'items'}
            # This would be expanded with actual item system
            if 'inventory' in player:
                player['inventory']['items'].append(item)
        
        return player

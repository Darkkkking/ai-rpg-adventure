import uuid
import json
import time
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import random

@dataclass
class GameSession:
    """Represents a multiplayer game session"""
    session_id: str
    host_player: str
    players: List[Dict[str, Any]]
    max_players: int
    status: str  # 'waiting', 'in_progress', 'completed'
    created_at: float
    current_quest: Optional[Dict[str, Any]] = None
    shared_story_context: Optional[List[Dict[str, Any]]] = None
    
    def __post_init__(self):
        if self.shared_story_context is None:
            self.shared_story_context = []

class MultiplayerSystem:
    """Handles multiplayer functionality for cooperative gameplay"""
    
    def __init__(self):
        self.active_sessions: Dict[str, GameSession] = {}
        self.player_sessions: Dict[str, str] = {}  # player_id -> session_id
        
        # Multiplayer quest templates designed for teams
        self.multiplayer_quests = [
            {
                'type': 'raid',
                'title_format': 'Raid the {creature} Den',
                'description_format': 'A pack of {creature}s has established a den {location}. This threat requires a coordinated team effort to eliminate.',
                'min_players': 2,
                'max_players': 4,
                'difficulty_modifier': 1.5,
                'rewards_multiplier': 1.3
            },
            {
                'type': 'siege',
                'title_format': 'Siege of the Ancient {creature}',
                'description_format': 'An enormous {creature} has claimed territory {location}. Only a united group of hunters can hope to defeat this legendary beast.',
                'min_players': 3,
                'max_players': 5,
                'difficulty_modifier': 2.0,
                'rewards_multiplier': 1.5
            },
            {
                'type': 'rescue',
                'title_format': 'Rescue Mission: {creature} Captives',
                'description_format': 'Villagers are trapped {location} by a {creature}. Time is critical - coordinate your assault to save them all.',
                'min_players': 2,
                'max_players': 4,
                'difficulty_modifier': 1.3,
                'rewards_multiplier': 1.2
            },
            {
                'type': 'defense',
                'title_format': 'Defend Against {creature} Horde',
                'description_format': 'Multiple {creature}s are advancing {location}. Form a defensive line and protect the innocent.',
                'min_players': 2,
                'max_players': 6,
                'difficulty_modifier': 1.4,
                'rewards_multiplier': 1.25
            }
        ]
    
    def create_session(self, host_player: Dict[str, Any], max_players: int = 4) -> str:
        """Create a new multiplayer session"""
        session_id = str(uuid.uuid4())[:8].upper()  # Short session ID
        
        session = GameSession(
            session_id=session_id,
            host_player=host_player['name'],
            players=[host_player],
            max_players=max_players,
            status='waiting',
            created_at=time.time()
        )
        
        self.active_sessions[session_id] = session
        self.player_sessions[host_player['name']] = session_id
        
        return session_id
    
    def join_session(self, session_id: str, player: Dict[str, Any]) -> bool:
        """Join an existing multiplayer session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        
        # Check if session is full or already started
        if len(session.players) >= session.max_players:
            return False
        
        if session.status != 'waiting':
            return False
        
        # Check if player is already in a session
        if player['name'] in self.player_sessions:
            return False
        
        # Add player to session
        session.players.append(player)
        self.player_sessions[player['name']] = session_id
        
        return True
    
    def leave_session(self, player_name: str) -> bool:
        """Leave a multiplayer session"""
        if player_name not in self.player_sessions:
            return False
        
        session_id = self.player_sessions[player_name]
        session = self.active_sessions[session_id]
        
        # Remove player from session
        session.players = [p for p in session.players if p['name'] != player_name]
        del self.player_sessions[player_name]
        
        # If host left, make someone else host or close session
        if session.host_player == player_name:
            if session.players:
                session.host_player = session.players[0]['name']
            else:
                # No players left, close session
                del self.active_sessions[session_id]
                return True
        
        # If no players left, close session
        if not session.players:
            del self.active_sessions[session_id]
        
        return True
    
    def start_session(self, session_id: str) -> bool:
        """Start a multiplayer session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        
        if session.status != 'waiting':
            return False
        
        if len(session.players) < 2:  # Need at least 2 players
            return False
        
        session.status = 'in_progress'
        return True
    
    def get_session(self, session_id: str) -> Optional[GameSession]:
        """Get session details"""
        return self.active_sessions.get(session_id)
    
    def get_player_session(self, player_name: str) -> Optional[GameSession]:
        """Get the session a player is currently in"""
        if player_name not in self.player_sessions:
            return None
        
        session_id = self.player_sessions[player_name]
        return self.active_sessions.get(session_id)
    
    def generate_multiplayer_quest(self, session: GameSession) -> Dict[str, Any]:
        """Generate a quest designed for multiplayer gameplay"""
        from quest_system import QuestSystem
        
        quest_system = QuestSystem()
        num_players = len(session.players)
        
        # Select appropriate multiplayer quest template
        suitable_quests = [
            q for q in self.multiplayer_quests 
            if q['min_players'] <= num_players <= q['max_players']
        ]
        
        if not suitable_quests:
            # Fallback to regular quest if no suitable multiplayer quest
            template = random.choice(quest_system.quest_templates)
        else:
            template = random.choice(suitable_quests)
        
        # Select creature based on average player level
        avg_level = sum(p['level'] for p in session.players) / len(session.players)
        avg_player = {'level': int(avg_level)}
        
        creature = quest_system._select_creature_for_player(avg_player)
        
        # Scale creature for multiplayer
        creature = self._scale_creature_for_multiplayer(creature, num_players, template.get('difficulty_modifier', 1.0))
        
        quest_giver = random.choice(quest_system.quest_givers)
        location = quest_system._generate_location()
        
        # Create multiplayer quest
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
            'multiplayer': True,
            'required_players': template.get('min_players', 2),
            'reward': self._calculate_multiplayer_rewards(
                session.players, 
                creature, 
                template.get('rewards_multiplier', 1.0)
            )
        }
        
        return quest
    
    def _scale_creature_for_multiplayer(self, creature: Dict[str, Any], num_players: int, difficulty_modifier: float) -> Dict[str, Any]:
        """Scale creature stats for multiplayer combat"""
        # Base scaling - creature gets stronger with more players
        player_scaling = 1 + (num_players - 1) * 0.4  # 40% increase per additional player
        total_modifier = player_scaling * difficulty_modifier
        
        creature['hp'] = int(creature['hp'] * total_modifier)
        creature['max_hp'] = creature['hp']
        creature['current_hp'] = creature['hp']
        creature['attack'] = int(creature['attack'] * (total_modifier * 0.8))  # Attack scales less
        creature['defense'] = int(creature['defense'] * (total_modifier * 0.6))  # Defense scales even less
        
        # Add multiplayer-specific abilities
        if num_players >= 3:
            creature['special_abilities'].append('Area Attack')
        if num_players >= 4:
            creature['special_abilities'].append('Regeneration')
        
        return creature
    
    def _calculate_multiplayer_rewards(self, players: List[Dict[str, Any]], creature: Dict[str, Any], rewards_multiplier: float) -> Dict[str, Any]:
        """Calculate rewards for multiplayer quests"""
        avg_level = sum(p['level'] for p in players) / len(players)
        base_gold = 40 + (avg_level * 20)
        base_exp = 30 + (avg_level * 15)
        
        # Difficulty modifiers
        difficulty_multipliers = {
            'easy': 0.8,
            'medium': 1.0,
            'hard': 1.3,
            'legendary': 1.6
        }
        
        multiplier = difficulty_multipliers.get(creature['difficulty'], 1.0) * rewards_multiplier
        
        # Each player gets individual rewards
        individual_rewards = {
            'gold': int(base_gold * multiplier),
            'experience': int(base_exp * multiplier),
            'items': []
        }
        
        # Bonus items for multiplayer
        if random.random() < 0.5:  # 50% chance for bonus items in multiplayer
            bonus_items = [
                f"Teamwork Medal",
                f"Cooperation Token",
                f"Guild Honor Badge",
                f"Multiplayer Achievement"
            ]
            individual_rewards['items'].extend(random.sample(bonus_items, random.randint(1, 2)))
        
        return individual_rewards
    
    def update_session_story(self, session_id: str, story_event: Dict[str, Any]) -> bool:
        """Update the shared story context for a session"""
        if session_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[session_id]
        if session.shared_story_context is None:
            session.shared_story_context = []
        session.shared_story_context.append(story_event)
        
        return True
    
    def get_session_stats(self, session_id: str) -> Dict[str, Any]:
        """Get statistics for a multiplayer session"""
        if session_id not in self.active_sessions:
            return {}
        
        session = self.active_sessions[session_id]
        
        total_level = sum(p['level'] for p in session.players)
        total_gold = sum(p['gold'] for p in session.players)
        total_quests = len([event for event in (session.shared_story_context or []) if event.get('type') == 'quest_completed'])
        
        stats = {
            'session_id': session_id,
            'num_players': len(session.players),
            'total_level': total_level,
            'average_level': total_level / len(session.players) if session.players else 0,
            'total_gold': total_gold,
            'quests_completed': total_quests,
            'session_duration': time.time() - session.created_at,
            'players': [{'name': p['name'], 'class': p['class'], 'level': p['level']} for p in session.players]
        }
        
        return stats
    
    def cleanup_expired_sessions(self, max_age_hours: int = 24):
        """Remove sessions that have been inactive for too long"""
        current_time = time.time()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if (current_time - session.created_at) > (max_age_hours * 3600):
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            session = self.active_sessions[session_id]
            # Remove player session mappings
            for player in session.players:
                if player['name'] in self.player_sessions:
                    del self.player_sessions[player['name']]
            # Remove session
            del self.active_sessions[session_id]
        
        return len(expired_sessions)
    
    def get_all_active_sessions(self) -> List[Dict[str, Any]]:
        """Get list of all active sessions for browsing"""
        sessions = []
        
        for session_id, session in self.active_sessions.items():
            if session.status == 'waiting':  # Only show joinable sessions
                sessions.append({
                    'session_id': session_id,
                    'host': session.host_player,
                    'players': len(session.players),
                    'max_players': session.max_players,
                    'created_at': session.created_at
                })
        
        return sessions
    
    def create_team_combat_state(self, session: GameSession, enemy: Dict[str, Any]) -> Dict[str, Any]:
        """Create a combat state for team-based combat"""
        combat_state = {
            'session_id': session.session_id,
            'players': [p.copy() for p in session.players],
            'enemy': enemy.copy(),
            'turn_order': self._determine_turn_order(session.players),
            'current_turn': 0,  # Index in turn_order
            'round': 1,
            'status': 'ongoing',
            'log': [f"Team combat begins! {len(session.players)} hunters vs {enemy['name']}"],
            'team_effects': {}  # For team buffs/debuffs
        }
        
        # Ensure all players have current_hp
        for player in combat_state['players']:
            if 'current_hp' not in player:
                player['current_hp'] = player['max_hp']
        
        # Ensure enemy has current_hp
        if 'current_hp' not in combat_state['enemy']:
            combat_state['enemy']['current_hp'] = combat_state['enemy']['max_hp']
        
        return combat_state
    
    def _determine_turn_order(self, players: List[Dict[str, Any]]) -> List[str]:
        """Determine turn order based on player agility"""
        # Sort players by agility (highest first)
        sorted_players = sorted(players, key=lambda p: p['stats']['agility'], reverse=True)
        turn_order = [p['name'] for p in sorted_players]
        
        # Add enemy turn after each player (interleaved)
        full_turn_order = []
        for player_name in turn_order:
            full_turn_order.append(player_name)
            full_turn_order.append('enemy')
        
        return full_turn_order
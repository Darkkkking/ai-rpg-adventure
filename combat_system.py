import random
from typing import Dict, Any, List

class CombatSystem:
    """Handles turn-based combat mechanics"""
    
    def __init__(self):
        pass
    
    def initialize_combat(self, player: Dict[str, Any], enemy: Dict[str, Any]) -> Dict[str, Any]:
        """Initialize a new combat encounter"""
        combat_state = {
            'player': player.copy(),
            'enemy': enemy.copy(),
            'turn': 'player',  # Player goes first
            'round': 1,
            'status': 'ongoing',
            'log': [f"Combat begins! {player['name']} vs {enemy['name']}"]
        }
        
        # Ensure both have current_hp set
        if 'current_hp' not in combat_state['player']:
            combat_state['player']['current_hp'] = combat_state['player']['max_hp']
        
        if 'current_hp' not in combat_state['enemy']:
            combat_state['enemy']['current_hp'] = combat_state['enemy']['max_hp']
        
        return combat_state
    
    def player_attack(self, combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute player attack"""
        player = combat_state['player']
        enemy = combat_state['enemy']
        
        # Calculate damage
        base_damage = self._calculate_player_damage(player)
        damage_dealt = max(1, base_damage - enemy.get('defense', 0))
        
        # Apply damage
        enemy['current_hp'] = max(0, enemy['current_hp'] - damage_dealt)
        
        # Log attack
        combat_state['log'].append(
            f"{player['name']} attacks {enemy['name']} for {damage_dealt} damage!"
        )
        
        # Check if enemy is defeated
        if enemy['current_hp'] <= 0:
            combat_state['status'] = 'victory'
            combat_state['log'].append(f"{enemy['name']} has been defeated!")
            return combat_state
        
        # Switch to enemy turn
        combat_state['turn'] = 'enemy'
        
        return combat_state
    
    def player_defend(self, combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute player defend action"""
        player = combat_state['player']
        
        # Defending reduces incoming damage and may restore some HP
        heal_amount = random.randint(5, 15)
        player['current_hp'] = min(player['max_hp'], player['current_hp'] + heal_amount)
        
        combat_state['log'].append(
            f"{player['name']} takes a defensive stance and recovers {heal_amount} HP!"
        )
        
        # Set defense boost for next enemy attack
        combat_state['player_defending'] = True
        
        # Switch to enemy turn
        combat_state['turn'] = 'enemy'
        
        return combat_state
    
    def enemy_turn(self, combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute enemy turn"""
        player = combat_state['player']
        enemy = combat_state['enemy']
        
        # Enemy AI - simple but effective
        action = self._determine_enemy_action(enemy, player)
        
        if action == 'attack':
            damage = self._calculate_enemy_damage(enemy)
            
            # Apply defense bonus if player was defending
            if combat_state.get('player_defending', False):
                damage = max(1, damage // 2)
                combat_state['log'].append(f"{player['name']}'s defense reduces incoming damage!")
                combat_state['player_defending'] = False
            
            # Apply player defense
            final_damage = max(1, damage - player['stats'].get('defense', 0))
            player['current_hp'] = max(0, player['current_hp'] - final_damage)
            
            combat_state['log'].append(
                f"{enemy['name']} attacks {player['name']} for {final_damage} damage!"
            )
            
            # Check if player is defeated
            if player['current_hp'] <= 0:
                combat_state['status'] = 'defeat'
                combat_state['log'].append(f"{player['name']} has been defeated!")
                return combat_state
        
        elif action == 'special':
            self._execute_enemy_special_ability(combat_state)
        
        # Switch back to player turn
        combat_state['turn'] = 'player'
        combat_state['round'] += 1
        
        return combat_state
    
    def _calculate_player_damage(self, player: Dict[str, Any]) -> int:
        """Calculate damage dealt by player"""
        base_damage = player['stats']['strength']
        
        # Add some randomness
        variance = random.randint(-3, 3)
        
        # Critical hit chance based on agility
        crit_chance = min(0.2, player['stats']['agility'] / 100)
        if random.random() < crit_chance:
            base_damage = int(base_damage * 1.5)
            variance = abs(variance)  # Ensure positive variance on crit
        
        return max(1, base_damage + variance)
    
    def _calculate_enemy_damage(self, enemy: Dict[str, Any]) -> int:
        """Calculate damage dealt by enemy"""
        base_damage = enemy['attack']
        variance = random.randint(-2, 2)
        return max(1, base_damage + variance)
    
    def _determine_enemy_action(self, enemy: Dict[str, Any], player: Dict[str, Any]) -> str:
        """Determine what action the enemy should take"""
        # Simple AI logic
        enemy_hp_ratio = enemy['current_hp'] / enemy['max_hp']
        
        # If enemy is low on health and has special abilities, use them more often
        if enemy_hp_ratio < 0.3 and enemy.get('special_abilities'):
            if random.random() < 0.6:  # 60% chance to use special when low HP
                return 'special'
        
        # Otherwise, mostly attack with occasional special abilities
        if enemy.get('special_abilities') and random.random() < 0.2:  # 20% chance
            return 'special'
        
        return 'attack'
    
    def _execute_enemy_special_ability(self, combat_state: Dict[str, Any]) -> None:
        """Execute a random special ability for the enemy"""
        enemy = combat_state['enemy']
        player = combat_state['player']
        
        if not enemy.get('special_abilities'):
            return
        
        ability = random.choice(enemy['special_abilities'])
        
        # Define special ability effects
        ability_effects = {
            'Crushing Bite': {
                'damage_multiplier': 1.5,
                'description': f"{enemy['name']} delivers a crushing bite!"
            },
            'Intimidating Roar': {
                'effect': 'stun',
                'description': f"{enemy['name']} lets out an intimidating roar!"
            },
            'Tusk Charge': {
                'damage_multiplier': 1.3,
                'description': f"{enemy['name']} charges with deadly tusks!"
            },
            'Pounce': {
                'damage_multiplier': 1.4,
                'description': f"{enemy['name']} pounces with feline grace!"
            },
            'Saber Strike': {
                'damage_multiplier': 1.6,
                'description': f"{enemy['name']} strikes with razor-sharp sabers!"
            },
            'Claw Swipe': {
                'damage_multiplier': 1.2,
                'description': f"{enemy['name']} swipes with massive claws!"
            },
            'Bear Hug': {
                'effect': 'grapple',
                'description': f"{enemy['name']} attempts to grapple!"
            },
            'Heavy Slam': {
                'damage_multiplier': 1.3,
                'description': f"{enemy['name']} slams down with tremendous force!"
            },
            'Piercing Beak': {
                'damage_multiplier': 1.5,
                'description': f"{enemy['name']} strikes with its piercing beak!"
            },
            'Swift Strike': {
                'damage_multiplier': 1.1,
                'hits': 2,
                'description': f"{enemy['name']} strikes twice in rapid succession!"
            },
            'Pack Howl': {
                'effect': 'buff',
                'description': f"{enemy['name']} howls, boosting its strength!"
            },
            'Venomous Bite': {
                'damage_multiplier': 1.2,
                'effect': 'poison',
                'description': f"{enemy['name']} bites with venomous fangs!"
            },
            'Tail Whip': {
                'damage_multiplier': 1.1,
                'description': f"{enemy['name']} lashes out with its powerful tail!"
            }
        }
        
        effect = ability_effects.get(ability, {
            'damage_multiplier': 1.2,
            'description': f"{enemy['name']} uses {ability}!"
        })
        
        combat_state['log'].append(effect['description'])
        
        # Apply effect
        if 'damage_multiplier' in effect:
            base_damage = self._calculate_enemy_damage(enemy)
            special_damage = int(base_damage * effect['damage_multiplier'])
            
            hits = effect.get('hits', 1)
            total_damage = 0
            
            for _ in range(hits):
                damage = max(1, special_damage - player['stats'].get('defense', 0))
                total_damage += damage
                player['current_hp'] = max(0, player['current_hp'] - damage)
            
            combat_state['log'].append(
                f"{player['name']} takes {total_damage} damage from {ability}!"
            )
        
        elif effect.get('effect') == 'stun':
            combat_state['log'].append(f"{player['name']} is intimidated and loses next turn!")
            # Could implement stun mechanics
        
        elif effect.get('effect') == 'buff':
            enemy['attack'] = int(enemy['attack'] * 1.1)
            combat_state['log'].append(f"{enemy['name']}'s attack power increases!")
        
        elif effect.get('effect') == 'poison':
            # Simple poison effect
            poison_damage = 5
            player['current_hp'] = max(0, player['current_hp'] - poison_damage)
            combat_state['log'].append(f"Poison deals {poison_damage} additional damage!")
    
    def get_combat_summary(self, combat_state: Dict[str, Any]) -> Dict[str, Any]:
        """Get a summary of the combat results"""
        return {
            'status': combat_state['status'],
            'rounds': combat_state['round'],
            'player_hp_remaining': combat_state['player']['current_hp'],
            'enemy_hp_remaining': combat_state['enemy']['current_hp'],
            'combat_log': combat_state['log']
        }

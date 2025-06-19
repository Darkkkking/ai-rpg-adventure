import plotly.graph_objects as go
from typing import Dict, Any, List, Tuple, Optional
import random

class GraphicsEngine:
    """Handles all graphics, animations, and visual elements for the RPG game"""
    
    def __init__(self):
        self.color_schemes = {
            'swordsman': {'primary': '#8B4513', 'secondary': '#C0C0C0', 'accent': '#FFD700'},
            'sniper': {'primary': '#228B22', 'secondary': '#8B4513', 'accent': '#FF4500'},
            'magician': {'primary': '#4B0082', 'secondary': '#9370DB', 'accent': '#FFD700'},
            'gunman': {'primary': '#2F4F4F', 'secondary': '#696969', 'accent': '#FF6347'},
            'archer': {'primary': '#006400', 'secondary': '#8FBC8F', 'accent': '#ADFF2F'},
            'warrior': {'primary': '#B22222', 'secondary': '#CD853F', 'accent': '#FFD700'},
            'hunter': {'primary': '#8B4513', 'secondary': '#DEB887', 'accent': '#32CD32'},
            'assassin': {'primary': '#2F2F2F', 'secondary': '#8B0000', 'accent': '#DC143C'},
            'hitman': {'primary': '#1C1C1C', 'secondary': '#696969', 'accent': '#FF1493'}
        }
        
        self.creature_colors = {
            'Tyrannosaurus Rex': '#8B4513',
            'Woolly Mammoth': '#D2B48C',
            'Saber-tooth Tiger': '#FF8C00',
            'Cave Bear': '#654321',
            'Giant Ground Sloth': '#A0522D',
            'Terror Bird': '#B22222',
            'Dire Wolf': '#2F4F4F',
            'Megalania': '#556B2F'
        }
    
    def create_character_avatar(self, character_class: str, name: str) -> str:
        """Create a visual avatar for character using SVG"""
        colors = self.color_schemes.get(character_class, self.color_schemes['warrior'])
        
        # Character icons and visual elements
        class_elements = {
            'swordsman': {'weapon': 'sword', 'armor': 'heavy', 'stance': 'combat'},
            'sniper': {'weapon': 'rifle', 'armor': 'light', 'stance': 'aiming'},
            'magician': {'weapon': 'staff', 'armor': 'robes', 'stance': 'casting'},
            'gunman': {'weapon': 'gun', 'armor': 'tactical', 'stance': 'ready'},
            'archer': {'weapon': 'bow', 'armor': 'leather', 'stance': 'drawn'},
            'warrior': {'weapon': 'shield', 'armor': 'plate', 'stance': 'defensive'},
            'hunter': {'weapon': 'spear', 'armor': 'camouflage', 'stance': 'tracking'},
            'assassin': {'weapon': 'dagger', 'armor': 'stealth', 'stance': 'hidden'},
            'hitman': {'weapon': 'pistol', 'armor': 'suit', 'stance': 'professional'}
        }
        
        elements = class_elements.get(character_class, class_elements['warrior'])
        
        svg_content = f"""
        <svg width="200" height="250" viewBox="0 0 200 250" xmlns="http://www.w3.org/2000/svg">
            <!-- Background circle -->
            <circle cx="100" cy="125" r="95" fill="{colors['primary']}" opacity="0.2"/>
            
            <!-- Character body -->
            <ellipse cx="100" cy="180" rx="40" ry="50" fill="{colors['primary']}"/>
            
            <!-- Character head -->
            <circle cx="100" cy="80" r="30" fill="#FDBCB4"/>
            
            <!-- Helmet/Hat based on class -->
            <ellipse cx="100" cy="65" rx="32" ry="20" fill="{colors['secondary']}"/>
            
            <!-- Class-specific weapon -->
            {self._get_weapon_svg(elements['weapon'], colors)}
            
            <!-- Character name -->
            <text x="100" y="230" text-anchor="middle" font-family="Arial, sans-serif" 
                  font-size="14" font-weight="bold" fill="{colors['accent']}">{name}</text>
            
            <!-- Class indicator -->
            <text x="100" y="245" text-anchor="middle" font-family="Arial, sans-serif" 
                  font-size="10" fill="{colors['primary']}">{character_class.upper()}</text>
        </svg>
        """
        
        return svg_content
    
    def _get_weapon_svg(self, weapon_type: str, colors: Dict[str, str]) -> str:
        """Generate SVG for different weapon types"""
        weapon_svg = {
            'sword': f'<rect x="95" y="120" width="10" height="60" fill="{colors["accent"]}" transform="rotate(15 100 150)"/>',
            'rifle': f'<rect x="85" y="135" width="30" height="6" fill="{colors["secondary"]}" transform="rotate(-15 100 138)"/>',
            'staff': f'<rect x="98" y="110" width="4" height="70" fill="{colors["accent"]}"/><circle cx="100" cy="110" r="8" fill="{colors["secondary"]}"/>',
            'gun': f'<rect x="90" y="140" width="20" height="8" fill="{colors["secondary"]}" transform="rotate(-10 100 144)"/>',
            'bow': f'<path d="M85,130 Q100,115 115,130" stroke="{colors["accent"]}" stroke-width="3" fill="none"/><line x1="85" y1="130" x2="115" y2="130" stroke="{colors["secondary"]}" stroke-width="2"/>',
            'shield': f'<ellipse cx="85" cy="140" rx="15" ry="25" fill="{colors["secondary"]}" transform="rotate(-20 85 140)"/>',
            'spear': f'<rect x="98" y="110" width="4" height="60" fill="{colors["accent"]}"/><polygon points="100,110 95,120 105,120" fill="{colors["secondary"]}"/>',
            'dagger': f'<rect x="97" y="130" width="6" height="25" fill="{colors["accent"]}" transform="rotate(25 100 142)"/>',
            'pistol': f'<rect x="92" y="142" width="16" height="6" fill="{colors["secondary"]}" transform="rotate(-5 100 145)"/>'
        }
        
        return weapon_svg.get(weapon_type, weapon_svg['sword'])
    
    def create_creature_visualization(self, creature: Dict[str, Any]) -> str:
        """Create a visual representation of creatures using SVG"""
        color = self.creature_colors.get(creature['name'], '#8B4513')
        
        # Creature-specific SVG designs
        creature_designs = {
            'Tyrannosaurus Rex': self._create_trex_svg(color),
            'Woolly Mammoth': self._create_mammoth_svg(color),
            'Saber-tooth Tiger': self._create_sabertooth_svg(color),
            'Cave Bear': self._create_bear_svg(color),
            'Giant Ground Sloth': self._create_sloth_svg(color),
            'Terror Bird': self._create_bird_svg(color),
            'Dire Wolf': self._create_wolf_svg(color),
            'Megalania': self._create_lizard_svg(color)
        }
        
        base_svg = f"""
        <svg width="300" height="200" viewBox="0 0 300 200" xmlns="http://www.w3.org/2000/svg">
            <!-- Background -->
            <rect width="300" height="200" fill="#2F4F2F" opacity="0.3"/>
            
            <!-- Ground -->
            <ellipse cx="150" cy="180" rx="120" ry="15" fill="#8B4513" opacity="0.6"/>
            
            {creature_designs.get(creature['name'], self._create_generic_creature_svg(color))}
            
            <!-- Creature name -->
            <text x="150" y="25" text-anchor="middle" font-family="Arial, sans-serif" 
                  font-size="16" font-weight="bold" fill="#FFD700">{creature['name']}</text>
            
            <!-- Difficulty indicator -->
            <text x="150" y="45" text-anchor="middle" font-family="Arial, sans-serif" 
                  font-size="12" fill="#FF6347">{creature['difficulty'].upper()}</text>
        </svg>
        """
        
        return base_svg
    
    def _create_trex_svg(self, color: str) -> str:
        """Create T-Rex SVG"""
        return f"""
        <!-- T-Rex body -->
        <ellipse cx="150" cy="120" rx="60" ry="40" fill="{color}"/>
        <!-- Head -->
        <ellipse cx="150" cy="80" rx="35" ry="25" fill="{color}"/>
        <!-- Jaw -->
        <path d="M115,85 L185,85 L180,95 L120,95 Z" fill="{color}" opacity="0.8"/>
        <!-- Teeth -->
        <polygon points="125,85 130,95 135,85" fill="white"/>
        <polygon points="140,85 145,95 150,85" fill="white"/>
        <polygon points="155,85 160,95 165,85" fill="white"/>
        <!-- Eyes -->
        <circle cx="135" cy="75" r="4" fill="red"/>
        <circle cx="165" cy="75" r="4" fill="red"/>
        <!-- Legs -->
        <rect x="130" y="150" width="15" height="25" fill="{color}"/>
        <rect x="155" y="150" width="15" height="25" fill="{color}"/>
        <!-- Arms -->
        <rect x="110" y="100" width="8" height="20" fill="{color}"/>
        <rect x="182" y="100" width="8" height="20" fill="{color}"/>
        <!-- Tail -->
        <ellipse cx="80" cy="130" rx="25" ry="8" fill="{color}"/>
        """
    
    def _create_mammoth_svg(self, color: str) -> str:
        """Create Mammoth SVG"""
        return f"""
        <!-- Mammoth body -->
        <ellipse cx="150" cy="130" rx="70" ry="35" fill="{color}"/>
        <!-- Head -->
        <circle cx="150" cy="90" r="30" fill="{color}"/>
        <!-- Tusks -->
        <ellipse cx="130" cy="100" rx="3" ry="20" fill="ivory" transform="rotate(-30 130 100)"/>
        <ellipse cx="170" cy="100" rx="3" ry="20" fill="ivory" transform="rotate(30 170 100)"/>
        <!-- Trunk -->
        <path d="M150,110 Q140,130 145,150" stroke="{color}" stroke-width="8" fill="none"/>
        <!-- Eyes -->
        <circle cx="135" cy="85" r="3" fill="black"/>
        <circle cx="165" cy="85" r="3" fill="black"/>
        <!-- Legs -->
        <rect x="120" y="155" width="12" height="20" fill="{color}"/>
        <rect x="140" y="155" width="12" height="20" fill="{color}"/>
        <rect x="160" y="155" width="12" height="20" fill="{color}"/>
        <rect x="180" y="155" width="12" height="20" fill="{color}"/>
        <!-- Fur texture -->
        <circle cx="130" cy="120" r="2" fill="#654321" opacity="0.6"/>
        <circle cx="170" cy="125" r="2" fill="#654321" opacity="0.6"/>
        <circle cx="150" cy="105" r="2" fill="#654321" opacity="0.6"/>
        """
    
    def _create_sabertooth_svg(self, color: str) -> str:
        """Create Saber-tooth Tiger SVG"""
        return f"""
        <!-- Tiger body -->
        <ellipse cx="150" cy="125" rx="45" ry="25" fill="{color}"/>
        <!-- Head -->
        <circle cx="150" cy="85" r="25" fill="{color}"/>
        <!-- Saber teeth -->
        <rect x="143" y="90" width="3" height="15" fill="white"/>
        <rect x="154" y="90" width="3" height="15" fill="white"/>
        <!-- Eyes -->
        <circle cx="140" cy="80" r="3" fill="yellow"/>
        <circle cx="160" cy="80" r="3" fill="yellow"/>
        <!-- Stripes -->
        <rect x="130" y="115" width="4" height="20" fill="#8B4513"/>
        <rect x="145" y="110" width="4" height="25" fill="#8B4513"/>
        <rect x="160" y="115" width="4" height="20" fill="#8B4513"/>
        <rect x="175" y="120" width="4" height="15" fill="#8B4513"/>
        <!-- Legs -->
        <rect x="130" y="145" width="10" height="20" fill="{color}"/>
        <rect x="150" y="145" width="10" height="20" fill="{color}"/>
        <rect x="170" y="145" width="10" height="20" fill="{color}"/>
        <!-- Tail -->
        <ellipse cx="105" cy="130" rx="20" ry="6" fill="{color}"/>
        """
    
    def _create_bear_svg(self, color: str) -> str:
        """Create Cave Bear SVG"""
        return f"""
        <!-- Bear body -->
        <ellipse cx="150" cy="130" rx="50" ry="30" fill="{color}"/>
        <!-- Head -->
        <circle cx="150" cy="85" r="25" fill="{color}"/>
        <!-- Ears -->
        <circle cx="135" cy="70" r="8" fill="{color}"/>
        <circle cx="165" cy="70" r="8" fill="{color}"/>
        <!-- Snout -->
        <ellipse cx="150" cy="95" rx="8" ry="5" fill="#654321"/>
        <!-- Eyes -->
        <circle cx="140" cy="80" r="3" fill="black"/>
        <circle cx="160" cy="80" r="3" fill="black"/>
        <!-- Legs -->
        <rect x="125" y="150" width="12" height="18" fill="{color}"/>
        <rect x="145" y="150" width="12" height="18" fill="{color}"/>
        <rect x="165" y="150" width="12" height="18" fill="{color}"/>
        <rect x="185" y="150" width="12" height="18" fill="{color}"/>
        <!-- Claws -->
        <rect x="125" y="168" width="2" height="5" fill="black"/>
        <rect x="130" y="168" width="2" height="5" fill="black"/>
        <rect x="135" y="168" width="2" height="5" fill="black"/>
        """
    
    def _create_sloth_svg(self, color: str) -> str:
        """Create Giant Ground Sloth SVG"""
        return f"""
        <!-- Sloth body -->
        <ellipse cx="150" cy="125" rx="55" ry="35" fill="{color}"/>
        <!-- Head -->
        <ellipse cx="150" cy="80" rx="20" ry="15" fill="{color}"/>
        <!-- Eyes -->
        <circle cx="145" cy="75" r="2" fill="black"/>
        <circle cx="155" cy="75" r="2" fill="black"/>
        <!-- Long arms -->
        <ellipse cx="110" cy="110" rx="8" ry="25" fill="{color}" transform="rotate(-30 110 110)"/>
        <ellipse cx="190" cy="110" rx="8" ry="25" fill="{color}" transform="rotate(30 190 110)"/>
        <!-- Claws -->
        <rect x="102" y="125" width="3" height="8" fill="black" transform="rotate(-30 104 129)"/>
        <rect x="186" y="125" width="3" height="8" fill="black" transform="rotate(30 188 129)"/>
        <!-- Legs -->
        <rect x="130" y="150" width="15" height="20" fill="{color}"/>
        <rect x="155" y="150" width="15" height="20" fill="{color}"/>
        <!-- Fur texture -->
        <circle cx="140" cy="115" r="1" fill="#654321" opacity="0.7"/>
        <circle cx="160" cy="120" r="1" fill="#654321" opacity="0.7"/>
        <circle cx="150" cy="135" r="1" fill="#654321" opacity="0.7"/>
        """
    
    def _create_bird_svg(self, color: str) -> str:
        """Create Terror Bird SVG"""
        return f"""
        <!-- Bird body -->
        <ellipse cx="150" cy="115" rx="35" ry="25" fill="{color}"/>
        <!-- Head -->
        <ellipse cx="150" cy="70" rx="18" ry="20" fill="{color}"/>
        <!-- Beak -->
        <polygon points="150,50 140,65 160,65" fill="#FFD700"/>
        <!-- Eyes -->
        <circle cx="145" cy="65" r="3" fill="red"/>
        <circle cx="155" cy="65" r="3" fill="red"/>
        <!-- Neck -->
        <rect x="145" y="85" width="10" height="15" fill="{color}"/>
        <!-- Legs -->
        <rect x="140" y="135" width="6" height="25" fill="#FFD700"/>
        <rect x="154" y="135" width="6" height="25" fill="#FFD700"/>
        <!-- Talons -->
        <polygon points="140,160 135,165 145,165" fill="black"/>
        <polygon points="154,160 149,165 159,165" fill="black"/>
        <!-- Wing -->
        <ellipse cx="120" cy="105" rx="15" ry="8" fill="{color}" opacity="0.8"/>
        <!-- Feather details -->
        <rect x="118" y="100" width="2" height="10" fill="#654321"/>
        <rect x="122" y="98" width="2" height="12" fill="#654321"/>
        """
    
    def _create_wolf_svg(self, color: str) -> str:
        """Create Dire Wolf SVG"""
        return f"""
        <!-- Wolf body -->
        <ellipse cx="150" cy="125" rx="40" ry="20" fill="{color}"/>
        <!-- Head -->
        <ellipse cx="150" cy="85" rx="20" ry="15" fill="{color}"/>
        <!-- Ears -->
        <polygon points="135,75 140,65 145,75" fill="{color}"/>
        <polygon points="155,75 160,65 165,75" fill="{color}"/>
        <!-- Snout -->
        <ellipse cx="150" cy="95" rx="6" ry="4" fill="#654321"/>
        <!-- Eyes -->
        <circle cx="145" cy="80" r="2" fill="yellow"/>
        <circle cx="155" cy="80" r="2" fill="yellow"/>
        <!-- Legs -->
        <rect x="130" y="140" width="8" height="20" fill="{color}"/>
        <rect x="145" y="140" width="8" height="20" fill="{color}"/>
        <rect x="160" y="140" width="8" height="20" fill="{color}"/>
        <rect x="175" y="140" width="8" height="20" fill="{color}"/>
        <!-- Tail -->
        <ellipse cx="110" cy="130" rx="15" ry="5" fill="{color}"/>
        <!-- Fur markings -->
        <ellipse cx="140" cy="115" rx="3" ry="6" fill="#1C1C1C" opacity="0.5"/>
        <ellipse cx="160" cy="120" rx="3" ry="6" fill="#1C1C1C" opacity="0.5"/>
        """
    
    def _create_lizard_svg(self, color: str) -> str:
        """Create Megalania SVG"""
        return f"""
        <!-- Lizard body -->
        <ellipse cx="150" cy="130" rx="60" ry="20" fill="{color}"/>
        <!-- Head -->
        <ellipse cx="150" cy="90" rx="25" ry="15" fill="{color}"/>
        <!-- Eyes -->
        <circle cx="140" cy="85" r="3" fill="orange"/>
        <circle cx="160" cy="85" r="3" fill="orange"/>
        <!-- Legs -->
        <ellipse cx="120" cy="145" rx="6" ry="12" fill="{color}"/>
        <ellipse cx="145" cy="145" rx="6" ry="12" fill="{color}"/>
        <ellipse cx="165" cy="145" rx="6" ry="12" fill="{color}"/>
        <ellipse cx="190" cy="145" rx="6" ry="12" fill="{color}"/>
        <!-- Tail -->
        <ellipse cx="90" cy="135" rx="25" ry="8" fill="{color}"/>
        <!-- Scales -->
        <circle cx="130" cy="125" r="2" fill="#2F4F2F" opacity="0.6"/>
        <circle cx="150" cy="120" r="2" fill="#2F4F2F" opacity="0.6"/>
        <circle cx="170" cy="125" r="2" fill="#2F4F2F" opacity="0.6"/>
        <circle cx="140" cy="135" r="2" fill="#2F4F2F" opacity="0.6"/>
        <circle cx="160" cy="135" r="2" fill="#2F4F2F" opacity="0.6"/>
        """
    
    def _create_generic_creature_svg(self, color: str) -> str:
        """Create generic creature SVG for unknown creatures"""
        return f"""
        <!-- Generic creature -->
        <ellipse cx="150" cy="125" rx="50" ry="25" fill="{color}"/>
        <circle cx="150" cy="85" r="20" fill="{color}"/>
        <circle cx="145" cy="80" r="3" fill="red"/>
        <circle cx="155" cy="80" r="3" fill="red"/>
        <rect x="135" y="140" width="10" height="18" fill="{color}"/>
        <rect x="155" y="140" width="10" height="18" fill="{color}"/>
        """
    
    def create_combat_visualization(self, combat_state: Dict[str, Any]) -> go.Figure:
        """Create an interactive combat visualization using Plotly"""
        player = combat_state['player']
        enemy = combat_state['enemy']
        
        # Create health bar visualization
        fig = go.Figure()
        
        # Player health bar
        player_hp_pct = player['current_hp'] / player['max_hp']
        fig.add_trace(go.Bar(
            x=[player_hp_pct * 100],
            y=['Player'],
            orientation='h',
            name=f"{player['name']} HP",
            marker_color='green' if player_hp_pct > 0.5 else 'orange' if player_hp_pct > 0.25 else 'red',
            text=f"{player['current_hp']}/{player['max_hp']}",
            textposition='inside'
        ))
        
        # Enemy health bar
        enemy_hp_pct = enemy['current_hp'] / enemy['max_hp']
        fig.add_trace(go.Bar(
            x=[enemy_hp_pct * 100],
            y=['Enemy'],
            orientation='h',
            name=f"{enemy['name']} HP",
            marker_color='red' if enemy_hp_pct > 0.5 else 'orange' if enemy_hp_pct > 0.25 else 'darkred',
            text=f"{enemy['current_hp']}/{enemy['max_hp']}",
            textposition='inside'
        ))
        
        fig.update_layout(
            title=f"Combat: {player['name']} vs {enemy['name']}",
            xaxis_title="Health %",
            xaxis=dict(range=[0, 100]),
            yaxis=dict(categoryorder='array', categoryarray=['Enemy', 'Player']),
            showlegend=False,
            height=300,
            font=dict(size=14)
        )
        
        return fig
    
    def create_character_stats_radar(self, character: Dict[str, Any]) -> go.Figure:
        """Create a radar chart showing character stats"""
        stats = character['stats']
        
        # Normalize stats for better visualization
        max_stat = max(stats.values())
        categories = list(stats.keys())
        values = [stats[cat] for cat in categories]
        
        # Close the radar chart
        categories += [categories[0]]
        values += [values[0]]
        
        fig = go.Figure()
        
        colors = self.color_schemes.get(character['class'], self.color_schemes['warrior'])
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=f"{character['name']} Stats",
            fillcolor=colors['primary'],
            line_color=colors['accent'],
            opacity=0.6
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max_stat * 1.2]
                )
            ),
            title=f"{character['name']} - {character['class'].title()} Stats",
            font=dict(size=12)
        )
        
        return fig
    
    def create_quest_progress_chart(self, story_context: List[Dict[str, Any]]) -> go.Figure:
        """Create a progress chart showing quest completions over time"""
        if not story_context:
            return go.Figure().add_annotation(text="No quest data available", 
                                            xref="paper", yref="paper", 
                                            x=0.5, y=0.5, showarrow=False)
        
        completed_quests = [ctx for ctx in story_context if ctx.get('type') == 'quest_completed']
        
        if not completed_quests:
            return go.Figure().add_annotation(text="No completed quests yet", 
                                            xref="paper", yref="paper", 
                                            x=0.5, y=0.5, showarrow=False)
        
        # Extract creature types and difficulties
        creatures = []
        difficulties = []
        quest_numbers = []
        
        for i, quest_ctx in enumerate(completed_quests, 1):
            quest = quest_ctx.get('quest', {})
            target = quest.get('target', {})
            creatures.append(target.get('name', 'Unknown'))
            difficulties.append(target.get('difficulty', 'unknown'))
            quest_numbers.append(i)
        
        # Create scatter plot
        difficulty_colors = {
            'easy': 'green',
            'medium': 'orange', 
            'hard': 'red',
            'legendary': 'purple',
            'unknown': 'gray'
        }
        
        colors = [difficulty_colors.get(diff, 'gray') for diff in difficulties]
        
        fig = go.Figure(data=go.Scatter(
            x=quest_numbers,
            y=creatures,
            mode='markers+lines',
            marker=dict(
                size=12,
                color=colors,
                line=dict(width=2, color='white')
            ),
            line=dict(width=2, color='gray', dash='dot'),
            text=[f"Quest {i}: {creature}<br>Difficulty: {diff}" 
                  for i, creature, diff in zip(quest_numbers, creatures, difficulties)],
            hovertemplate='%{text}<extra></extra>'
        ))
        
        fig.update_layout(
            title="Quest Completion Progress",
            xaxis_title="Quest Number",
            yaxis_title="Creatures Defeated",
            height=400,
            font=dict(size=12)
        )
        
        return fig
    
    def create_multiplayer_lobby_display(self, players: List[Dict[str, Any]]) -> str:
        """Create a visual display for multiplayer lobby"""
        if not players:
            return """
            <div style="text-align: center; padding: 20px; border: 2px dashed #ccc; border-radius: 10px;">
                <h3>🏰 Multiplayer Lobby</h3>
                <p>Waiting for adventurers to join...</p>
                <p style="color: #666;">Share your lobby code with friends!</p>
            </div>
            """
        
        player_cards = ""
        for i, player in enumerate(players):
            colors = self.color_schemes.get(player['class'], self.color_schemes['warrior'])
            player_cards += f"""
            <div style="
                display: inline-block; 
                margin: 10px; 
                padding: 15px; 
                border: 2px solid {colors['primary']}; 
                border-radius: 10px; 
                background: linear-gradient(45deg, {colors['primary']}20, {colors['secondary']}20);
                text-align: center;
                min-width: 150px;
            ">
                <h4 style="margin: 0; color: {colors['primary']};">{player['name']}</h4>
                <p style="margin: 5px 0; color: {colors['accent']}; font-weight: bold;">
                    {player['class'].title()}
                </p>
                <p style="margin: 5px 0; font-size: 0.9em;">
                    Level {player['level']} | {player['gold']} Gold
                </p>
                <div style="
                    background: {colors['primary']}40; 
                    padding: 5px; 
                    border-radius: 5px; 
                    margin-top: 10px;
                ">
                    Ready for Adventure!
                </div>
            </div>
            """
        
        return f"""
        <div style="text-align: center; padding: 20px;">
            <h3>🏰 Monster Hunters Guild - Multiplayer Lobby</h3>
            <p>Brave adventurers assembled for cooperative hunts:</p>
            <div style="margin: 20px 0;">
                {player_cards}
            </div>
            <p style="color: #666; font-style: italic;">
                Ready to face ancient beasts together!
            </p>
        </div>
        """
    
    def create_kingdom_map(self, visited_locations: Optional[List[str]] = None) -> str:
        """Create an SVG map of the kingdom showing visited locations"""
        if visited_locations is None:
            visited_locations = []
        
        # Define locations with coordinates
        locations = {
            'Ancient Forest': (100, 80),
            'Forgotten Ruins': (200, 60),
            'Mountain Pass': (150, 40),
            'Mystic Lake': (80, 120),
            'Dark Caverns': (250, 100),
            'Village Outskirts': (150, 150),
            'Old Watchtower': (300, 80),
            'Haunted Valley': (50, 160),
            'Crossroads': (150, 120),
            'River Bend': (120, 180),
            'Stone Circle': (220, 140),
            'Abandoned Mine': (280, 140),
            'Crystal Falls': (80, 50),
            'Whispering Woods': (180, 180),
            'Merchant\'s Route': (200, 120)
        }
        
        map_svg = f"""
        <svg width="400" height="250" viewBox="0 0 400 250" xmlns="http://www.w3.org/2000/svg">
            <!-- Background -->
            <rect width="400" height="250" fill="#2F5233" opacity="0.3"/>
            
            <!-- Terrain features -->
            <!-- Mountains -->
            <polygon points="120,20 150,50 180,20 200,40 250,10 280,30 320,5 350,25 380,15 400,30 400,0 0,0 0,40" 
                     fill="#8B7355" opacity="0.7"/>
            
            <!-- Forest -->
            <circle cx="100" cy="80" r="25" fill="#228B22" opacity="0.6"/>
            <circle cx="85" cy="95" r="20" fill="#228B22" opacity="0.6"/>
            <circle cx="115" cy="95" r="20" fill="#228B22" opacity="0.6"/>
            
            <!-- Lake -->
            <ellipse cx="80" cy="120" rx="30" ry="15" fill="#4682B4" opacity="0.7"/>
            
            <!-- Roads -->
            <path d="M0,120 Q100,110 150,120 Q200,130 400,120" stroke="#8B4513" stroke-width="3" 
                  fill="none" opacity="0.5"/>
            <path d="M150,120 L150,250" stroke="#8B4513" stroke-width="2" fill="none" opacity="0.5"/>
            
            <!-- Kingdom Castle (Center) -->
            <rect x="140" y="110" width="20" height="20" fill="#FFD700"/>
            <polygon points="150,105 145,115 155,115" fill="#B8860B"/>
            <text x="150" y="145" text-anchor="middle" font-family="Arial" font-size="10" 
                  fill="#FFD700" font-weight="bold">Kingdom</text>
        """
        
        # Add location markers
        for location, (x, y) in locations.items():
            visited = location in visited_locations
            color = "#FF6347" if visited else "#696969"
            opacity = "1.0" if visited else "0.5"
            
            map_svg += f"""
            <!-- {location} -->
            <circle cx="{x}" cy="{y}" r="4" fill="{color}" opacity="{opacity}"/>
            <text x="{x}" y="{y-8}" text-anchor="middle" font-family="Arial" font-size="8" 
                  fill="{color}" opacity="{opacity}">{location.split()[0]}</text>
            """
        
        map_svg += """
            <!-- Legend -->
            <rect x="10" y="200" width="120" height="40" fill="white" opacity="0.8" stroke="black"/>
            <text x="15" y="215" font-family="Arial" font-size="10" font-weight="bold">Legend:</text>
            <circle cx="20" cy="225" r="3" fill="#FF6347"/>
            <text x="30" y="228" font-family="Arial" font-size="9">Visited</text>
            <circle cx="20" cy="235" r="3" fill="#696969" opacity="0.5"/>
            <text x="30" y="238" font-family="Arial" font-size="9">Unexplored</text>
        </svg>
        """
        
        return map_svg
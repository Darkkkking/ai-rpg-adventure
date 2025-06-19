import streamlit as st
import json
import plotly.graph_objects as go
from game_engine import GameEngine
from character_system import CharacterSystem
from quest_system import QuestSystem
from combat_system import CombatSystem
from ai_story_generator import AIStoryGenerator
from data_manager import DataManager
from graphics_engine import GraphicsEngine
from multiplayer_system import MultiplayerSystem

# Initialize game components
@st.cache_resource
def initialize_game():
    return GameEngine()

@st.cache_resource
def initialize_graphics():
    return GraphicsEngine()

@st.cache_resource  
def initialize_multiplayer():
    return MultiplayerSystem()

def main():
    st.set_page_config(
        page_title="AI RPG Adventure",
        page_icon="⚔️",
        layout="wide"
    )
    
    # Initialize game systems
    game = initialize_game()
    graphics = initialize_graphics()
    multiplayer = initialize_multiplayer()
    
    # Initialize session state
    if 'game_state' not in st.session_state:
        st.session_state.game_state = 'menu'
    if 'player' not in st.session_state:
        st.session_state.player = None
    if 'current_quest' not in st.session_state:
        st.session_state.current_quest = None
    if 'combat_state' not in st.session_state:
        st.session_state.combat_state = None
    if 'story_context' not in st.session_state:
        st.session_state.story_context = []
    if 'multiplayer_session' not in st.session_state:
        st.session_state.multiplayer_session = None
    if 'visited_locations' not in st.session_state:
        st.session_state.visited_locations = []
    
    # Main title
    st.title("⚔️ AI-Powered RPG Adventure")
    st.markdown("*Defend the Kingdom Against Ancient Beasts*")
    
    # Game state management
    if st.session_state.game_state == 'menu':
        show_main_menu(game)
    elif st.session_state.game_state == 'character_creation':
        show_character_creation(game, graphics)
    elif st.session_state.game_state == 'playing':
        show_game_interface(game, graphics, multiplayer)
    elif st.session_state.game_state == 'combat':
        show_combat_interface(game, graphics)
    elif st.session_state.game_state == 'quest_complete':
        show_quest_completion(game, graphics)

def show_main_menu(game):
    st.header("🏰 Welcome to the Kingdom")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### The Ancient Threat Returns
        
        Extinct creatures from the dawn of time have mysteriously returned to terrorize our kingdom. 
        As a member of the elite Monster Hunters Guild, you must embark on dangerous quests to 
        protect our people and uncover the source of this ancient evil.
        
        Choose your path wisely, brave adventurer...
        """)
        
        if st.session_state.player is None:
            if st.button("🎯 Create New Character", use_container_width=True):
                st.session_state.game_state = 'character_creation'
                st.rerun()
        else:
            st.success(f"Welcome back, {st.session_state.player['name']} the {st.session_state.player['class']}!")
            if st.button("🎮 Continue Adventure", use_container_width=True):
                st.session_state.game_state = 'playing'
                st.rerun()
            
            if st.button("🔄 Create New Character", use_container_width=True):
                st.session_state.player = None
                st.session_state.game_state = 'character_creation'
                st.rerun()

def show_character_creation(game, graphics):
    st.header("🎭 Create Your Character")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Character Details")
        name = st.text_input("Character Name", placeholder="Enter your hero's name")
        
        st.subheader("Choose Your Class")
        character_classes = game.character_system.get_available_classes()
        
        selected_class = st.selectbox(
            "Class",
            options=list(character_classes.keys()),
            format_func=lambda x: f"{character_classes[x]['icon']} {x.title()}"
        )
        
        if selected_class:
            class_info = character_classes[selected_class]
            st.markdown(f"**{class_info['description']}**")
            
            st.markdown("**Starting Stats:**")
            for stat, value in class_info['base_stats'].items():
                st.write(f"• {stat.replace('_', ' ').title()}: {value}")
            
            st.markdown("**Special Abilities:**")
            for ability in class_info['abilities']:
                st.write(f"• {ability}")
    
    with col2:
        if selected_class:
            st.subheader("Class Preview")
            class_info = character_classes[selected_class]
            st.markdown(f"### {class_info['icon']} {selected_class.title()}")
            st.markdown(class_info['lore'])
            
            # Display character avatar
            graphics = initialize_graphics()
            avatar_svg = graphics.create_character_avatar(selected_class, name if name else "Hero")
            st.markdown(avatar_svg, unsafe_allow_html=True)
    
    if st.button("⚔️ Begin Adventure", disabled=not name or not selected_class):
        # Create character
        player = game.character_system.create_character(name, selected_class)
        st.session_state.player = player
        st.session_state.game_state = 'playing'
        st.success(f"Welcome, {name} the {selected_class}!")
        st.rerun()

def show_game_interface(game, graphics, multiplayer):
    if not st.session_state.player:
        st.session_state.game_state = 'menu'
        st.rerun()
        return
    
    player = st.session_state.player
    
    # Header with character info
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        st.subheader(f"{player['name']} the {player['class'].title()}")
    
    with col2:
        st.metric("Level", player['level'])
    
    with col3:
        st.metric("XP", f"{player['experience']}/{player['experience_to_next']}")
    
    with col4:
        st.metric("Gold", player['gold'])
    
    # Main game tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🏹 Quests", "📦 Inventory", "📊 Character", "🏰 Guild", "🎮 Multiplayer", "🗺️ Map"])
    
    with tab1:
        show_quest_interface(game, graphics)
    
    with tab2:
        show_inventory_interface(game, graphics)
    
    with tab3:
        show_character_interface(game, graphics)
    
    with tab4:
        show_guild_interface(game, graphics)
    
    with tab5:
        show_multiplayer_interface(game, graphics, multiplayer)
    
    with tab6:
        show_map_interface(game, graphics)

def show_quest_interface(game, graphics):
    st.subheader("🏹 Monster Hunting Quests")
    
    if st.session_state.current_quest is None:
        st.markdown("### Available Quests")
        
        if st.button("🎲 Generate New Quest"):
            # Generate AI-powered quest
            quest = game.quest_system.generate_quest(st.session_state.player, st.session_state.story_context)
            st.session_state.current_quest = quest
            st.rerun()
        
        # Show some default quests if no current quest
        st.markdown("""
        **The Monster Hunters Guild has urgent missions available:**
        
        📜 Click "Generate New Quest" to receive your next AI-generated mission
        🤖 Each quest is dynamically created based on your character and story progression
        ⚔️ Face extinct ancient creatures in turn-based combat
        🏆 Earn rewards, experience, and advance the kingdom's story
        """)
    
    else:
        quest = st.session_state.current_quest
        st.markdown(f"### {quest['title']}")
        st.markdown(f"**Quest Giver:** {quest['giver']}")
        st.markdown(f"**Description:** {quest['description']}")
        st.markdown(f"**Target:** {quest['target']['name']}")
        st.markdown(f"**Reward:** {quest['reward']['gold']} gold, {quest['reward']['experience']} XP")
        
        if quest['reward'].get('items'):
            st.markdown(f"**Items:** {', '.join(quest['reward']['items'])}")
        
        # Display creature visualization
        creature_svg = graphics.create_creature_visualization(quest['target'])
        st.markdown(creature_svg, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("⚔️ Begin Hunt"):
                st.session_state.combat_state = game.combat_system.initialize_combat(
                    st.session_state.player, 
                    quest['target']
                )
                st.session_state.game_state = 'combat'
                st.rerun()
        
        with col2:
            if st.button("❌ Abandon Quest"):
                st.session_state.current_quest = None
                st.rerun()

def show_combat_interface(game, graphics):
    if not st.session_state.combat_state:
        st.session_state.game_state = 'playing'
        st.rerun()
        return
    
    combat = st.session_state.combat_state
    player = combat['player']
    enemy = combat['enemy']
    
    st.header("⚔️ Combat")
    st.markdown(f"**{player['name']}** vs **{enemy['name']}**")
    
    # Health bars
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Your Health")
        health_pct = player['current_hp'] / player['max_hp']
        st.progress(health_pct)
        st.write(f"{player['current_hp']}/{player['max_hp']} HP")
    
    with col2:
        st.subheader("Enemy Health")
        enemy_health_pct = enemy['current_hp'] / enemy['max_hp']
        st.progress(enemy_health_pct)
        st.write(f"{enemy['current_hp']}/{enemy['max_hp']} HP")
    
    # Combat visualization
    combat_fig = graphics.create_combat_visualization(combat)
    st.plotly_chart(combat_fig, use_container_width=True)
    
    # Combat log
    if combat.get('log'):
        st.subheader("Combat Log")
        for entry in combat['log'][-5:]:  # Show last 5 entries
            st.write(entry)
    
    # Combat actions
    if combat['turn'] == 'player':
        st.subheader("Your Turn")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("⚔️ Attack"):
                result = game.combat_system.player_attack(combat)
                st.session_state.combat_state = result
                if result['status'] in ['victory', 'defeat']:
                    handle_combat_end(game, result)
                st.rerun()
        
        with col2:
            if st.button("🛡️ Defend"):
                result = game.combat_system.player_defend(combat)
                st.session_state.combat_state = result
                st.rerun()
        
        with col3:
            # Check if player has healing items or abilities
            if st.button("💊 Use Item", disabled=True):  # Placeholder for item usage
                st.info("Item usage coming soon!")
    
    else:
        st.subheader("Enemy Turn")
        if st.button("⏩ Continue"):
            result = game.combat_system.enemy_turn(combat)
            st.session_state.combat_state = result
            if result['status'] in ['victory', 'defeat']:
                handle_combat_end(game, result)
            st.rerun()

def handle_combat_end(game, result):
    if result['status'] == 'victory':
        # Award quest rewards
        quest = st.session_state.current_quest
        player = st.session_state.player
        
        # Update player with rewards
        player['gold'] += quest['reward']['gold']
        player['experience'] += quest['reward']['experience']
        
        # Check for level up
        if player['experience'] >= player['experience_to_next']:
            game.character_system.level_up(player)
        
        # Add quest to completed quests and story context
        st.session_state.story_context.append({
            'type': 'quest_completed',
            'quest': quest,
            'outcome': 'victory'
        })
        
        st.session_state.current_quest = None
        st.session_state.combat_state = None
        st.session_state.game_state = 'quest_complete'
    
    else:  # defeat
        st.session_state.combat_state = None
        st.session_state.game_state = 'playing'
        # Could implement death penalties here

def show_quest_completion(game, graphics):
    st.header("🏆 Quest Complete!")
    
    quest = st.session_state.story_context[-1]['quest'] if st.session_state.story_context else None
    
    if quest:
        st.success(f"**{quest['title']}** completed successfully!")
        st.markdown(f"**Rewards Earned:**")
        st.write(f"• {quest['reward']['gold']} Gold")
        st.write(f"• {quest['reward']['experience']} Experience")
        
        if quest['reward'].get('items'):
            st.write(f"• Items: {', '.join(quest['reward']['items'])}")
    
    # Generate quest completion story
    if st.button("📖 Generate Completion Story"):
        story = game.ai_story_generator.generate_quest_completion_story(
            st.session_state.player,
            quest,
            st.session_state.story_context
        )
        st.markdown("### 📜 Your Tale")
        st.markdown(story)
    
    if st.button("🏰 Return to Guild"):
        st.session_state.game_state = 'playing'
        st.rerun()

def show_inventory_interface(game, graphics):
    st.subheader("📦 Inventory")
    player = st.session_state.player
    
    if not player.get('inventory'):
        st.info("Your inventory is empty. Complete quests to earn items!")
        return
    
    # Display inventory items
    for category, items in player['inventory'].items():
        if items:
            st.markdown(f"**{category.title()}:**")
            for item in items:
                st.write(f"• {item}")

def show_character_interface(game, graphics):
    st.subheader("📊 Character Stats")
    player = st.session_state.player
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Core Stats:**")
        for stat, value in player['stats'].items():
            st.metric(stat.replace('_', ' ').title(), value)
    
    with col2:
        st.markdown("**Progress:**")
        st.metric("Level", player['level'])
        st.metric("Experience", f"{player['experience']}/{player['experience_to_next']}")
        st.metric("Gold", player['gold'])
        
        # Experience progress bar
        exp_progress = player['experience'] / player['experience_to_next']
        st.progress(exp_progress)
    
    # Character stats radar chart
    st.subheader("📈 Stats Visualization")
    radar_fig = graphics.create_character_stats_radar(player)
    st.plotly_chart(radar_fig, use_container_width=True)

def show_guild_interface(game, graphics):
    st.subheader("🏰 Monster Hunters Guild")
    
    st.markdown("""
    ### Welcome to the Guild Hall
    
    The Monster Hunters Guild is your home base for receiving quests, 
    trading items, and learning about the ancient threat facing our kingdom.
    
    **Guild Services:**
    • Quest Assignment (Available in Quests tab)
    • Item Trading (Coming Soon)
    • Guild Rankings (Coming Soon)
    • Lore Library (Coming Soon)
    """)
    
    if st.session_state.story_context:
        st.markdown("### Your Adventures")
        completed_quests = [ctx for ctx in st.session_state.story_context if ctx['type'] == 'quest_completed']
        st.write(f"Quests Completed: {len(completed_quests)}")
        
        if completed_quests:
            st.markdown("**Recent Victories:**")
            for quest_ctx in completed_quests[-3:]:  # Show last 3
                quest = quest_ctx['quest']
                st.write(f"• Defeated {quest['target']['name']} - {quest['title']}")
    
    # Quest progress visualization
    if st.session_state.story_context:
        st.subheader("📈 Quest Progress")
        progress_fig = graphics.create_quest_progress_chart(st.session_state.story_context)
        st.plotly_chart(progress_fig, use_container_width=True)

def show_multiplayer_interface(game, graphics, multiplayer):
    st.subheader("🎮 Multiplayer Adventures")
    
    player = st.session_state.player
    if not player:
        st.warning("Create a character first to join multiplayer sessions!")
        return
    
    # Check if player is in a session
    current_session = multiplayer.get_player_session(player['name'])
    
    if current_session is None:
        # Player not in session - show options to create or join
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Create New Session")
            max_players = st.selectbox("Max Players", [2, 3, 4, 5, 6], index=1)
            
            if st.button("🏰 Create Session"):
                session_id = multiplayer.create_session(player, max_players)
                st.session_state.multiplayer_session = session_id
                st.success(f"Session created! ID: {session_id}")
                st.rerun()
        
        with col2:
            st.markdown("### Join Existing Session")
            session_id = st.text_input("Session ID")
            
            if st.button("🚪 Join Session") and session_id:
                if multiplayer.join_session(session_id, player):
                    st.session_state.multiplayer_session = session_id
                    st.success(f"Joined session {session_id}!")
                    st.rerun()
                else:
                    st.error("Could not join session. Check ID or session may be full.")
        
        # Show available sessions
        st.markdown("### Available Sessions")
        sessions = multiplayer.get_all_active_sessions()
        
        if sessions:
            for session in sessions:
                with st.expander(f"Session {session['session_id']} - {session['players']}/{session['max_players']} players"):
                    st.write(f"Host: {session['host']}")
                    if st.button(f"Join {session['session_id']}", key=f"join_{session['session_id']}"):
                        if multiplayer.join_session(session['session_id'], player):
                            st.session_state.multiplayer_session = session['session_id']
                            st.success(f"Joined session!")
                            st.rerun()
        else:
            st.info("No available sessions. Create one to start!")
    
    else:
        # Player is in a session - show session interface
        st.markdown(f"### Session: {current_session.session_id}")
        
        # Display session members
        lobby_html = graphics.create_multiplayer_lobby_display(current_session.players)
        st.markdown(lobby_html, unsafe_allow_html=True)
        
        # Session controls
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if current_session.host_player == player['name'] and current_session.status == 'waiting':
                if st.button("🚀 Start Adventure") and len(current_session.players) >= 2:
                    multiplayer.start_session(current_session.session_id)
                    st.success("Adventure started!")
                    st.rerun()
        
        with col2:
            if current_session.status == 'in_progress':
                if st.button("🏹 Generate Team Quest"):
                    team_quest = multiplayer.generate_multiplayer_quest(current_session)
                    st.session_state.current_quest = team_quest
                    st.success("Team quest generated!")
        
        with col3:
            if st.button("🚪 Leave Session"):
                multiplayer.leave_session(player['name'])
                st.session_state.multiplayer_session = None
                st.success("Left session")
                st.rerun()
        
        # Show session stats
        if current_session.status == 'in_progress':
            stats = multiplayer.get_session_stats(current_session.session_id)
            st.markdown("### Team Statistics")
            
            stat_col1, stat_col2, stat_col3 = st.columns(3)
            with stat_col1:
                st.metric("Team Size", stats['num_players'])
            with stat_col2:
                st.metric("Average Level", f"{stats['average_level']:.1f}")
            with stat_col3:
                st.metric("Quests Completed", stats['quests_completed'])

def show_map_interface(game, graphics):
    st.subheader("🗺️ Kingdom Map")
    
    # Add current quest location to visited if quest exists
    if st.session_state.current_quest and st.session_state.current_quest.get('location'):
        location = st.session_state.current_quest['location']
        if location not in st.session_state.visited_locations:
            st.session_state.visited_locations.append(location)
    
    # Create and display kingdom map
    map_svg = graphics.create_kingdom_map(st.session_state.visited_locations)
    st.markdown(map_svg, unsafe_allow_html=True)
    
    st.markdown("### Exploration Progress")
    
    # Show exploration statistics
    total_locations = 15  # Total locations in the game
    visited_count = len(st.session_state.visited_locations)
    exploration_pct = (visited_count / total_locations) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Locations Visited", visited_count)
    with col2:
        st.metric("Total Locations", total_locations)
    with col3:
        st.metric("Exploration", f"{exploration_pct:.1f}%")
    
    st.progress(exploration_pct / 100)
    
    if st.session_state.visited_locations:
        st.markdown("### Recent Expeditions")
        for location in st.session_state.visited_locations[-5:]:
            st.write(f"📍 {location}")

if __name__ == "__main__":
    main()

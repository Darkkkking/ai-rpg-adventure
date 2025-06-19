import json
import os
import random
from typing import Dict, Any, List, Optional
from openai import OpenAI

class AIStoryGenerator:
    """Handles AI-powered story and quest generation using OpenAI"""
    
    def __init__(self):
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        self.openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "default_key")
        )
        self.model = "gpt-4o"
        
        # Story themes and elements
        self.story_themes = [
            "ancient_awakening",
            "time_rift",
            "forgotten_magic",
            "cursed_artifact",
            "dimensional_breach",
            "prehistoric_resurrection"
        ]
    
    def enhance_quest(self, base_quest: Dict[str, Any], player: Dict[str, Any], story_context: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Use AI to enhance a quest with rich story elements"""
        try:
            # Prepare context for AI
            context_summary = self._prepare_story_context(story_context)
            
            prompt = f"""
            You are a master storyteller creating an engaging RPG quest. 
            
            Player Character:
            - Name: {player['name']}
            - Class: {player['class']}
            - Level: {player['level']}
            
            Base Quest:
            - Title: {base_quest['title']}
            - Target: {base_quest['target']['name']}
            - Location: {base_quest['location']}
            - Quest Giver: {base_quest['giver']}
            
            Story Context: {context_summary}
            
            Please enhance this quest with:
            1. Rich narrative description that fits the Monster Hunters Guild setting
            2. Compelling backstory for why this creature appeared
            3. Emotional stakes that make the player care
            4. Atmospheric details about the location and encounter
            
            Return a JSON object with these fields:
            - "enhanced_description": A more engaging quest description
            - "backstory": Why this creature has appeared now
            - "atmospheric_details": Details about the location and mood
            - "stakes": Why this quest matters to the kingdom
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert RPG quest writer specializing in monster hunting adventures."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                max_tokens=500
            )
            
            enhancement = json.loads(response.choices[0].message.content)
            return enhancement
            
        except Exception as e:
            print(f"AI quest enhancement failed: {e}")
            return None
    
    def generate_quest_completion_story(self, player: Dict[str, Any], quest: Dict[str, Any], story_context: List[Dict[str, Any]]) -> str:
        """Generate a story for quest completion"""
        try:
            context_summary = self._prepare_story_context(story_context)
            
            prompt = f"""
            Write a short, engaging story about {player['name']} the {player['class']} successfully completing their quest to defeat the {quest['target']['name']}.
            
            Quest Details:
            - Location: {quest['location']}
            - Quest Giver: {quest['giver']}
            
            Story Context: {context_summary}
            
            Write this as a heroic tale in 2-3 paragraphs, focusing on:
            1. The final confrontation with the creature
            2. How the player's class abilities were crucial to victory  
            3. The impact on the kingdom and people
            4. A hint at the larger mystery of why these creatures are returning
            
            Write in an engaging, epic fantasy style.
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a master storyteller writing epic fantasy tales."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=400
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Story generation failed: {e}")
            return self._generate_fallback_completion_story(player, quest)
    
    def generate_random_encounter_story(self, player: Dict[str, Any], location: str) -> str:
        """Generate a random encounter story"""
        try:
            prompt = f"""
            Create a brief, atmospheric description of {player['name']} the {player['class']} 
            exploring {location} in a fantasy world where ancient creatures have mysteriously returned.
            
            Include:
            - Atmospheric details about the location
            - Signs of ancient creature activity
            - A sense of mystery and danger
            - Class-appropriate observations (what would a {player['class']} notice?)
            
            Keep it to 1-2 paragraphs and maintain an air of mystery.
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are writing atmospheric descriptions for an RPG game."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Encounter story generation failed: {e}")
            return self._generate_fallback_encounter_story(location)
    
    def generate_overarching_plot_development(self, story_context: List[Dict[str, Any]]) -> str:
        """Generate plot development based on completed quests"""
        if len(story_context) < 3:
            return ""
        
        try:
            context_summary = self._prepare_story_context(story_context)
            
            prompt = f"""
            Based on the player's adventures so far, generate a plot development that reveals 
            more about why ancient extinct creatures are returning to threaten the kingdom.
            
            Previous Adventures: {context_summary}
            
            Create a revelation or plot twist that:
            1. Connects the recent creature encounters
            2. Hints at a larger threat or conspiracy
            3. Sets up future adventures
            4. Maintains mystery while providing some answers
            
            Write as a dramatic revelation in 2-3 sentences.
            """
            
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are crafting an overarching plot for an RPG campaign."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Plot development generation failed: {e}")
            return ""
    
    def _prepare_story_context(self, story_context: List[Dict[str, Any]]) -> str:
        """Prepare story context for AI prompts"""
        if not story_context:
            return "This is the player's first adventure."
        
        completed_quests = [ctx for ctx in story_context if ctx.get('type') == 'quest_completed']
        
        if not completed_quests:
            return "The player is just beginning their journey as a Monster Hunter."
        
        context_parts = []
        for quest_ctx in completed_quests[-3:]:  # Last 3 quests
            quest = quest_ctx.get('quest', {})
            creature_name = quest.get('target', {}).get('name', 'unknown creature')
            location = quest.get('location', 'unknown location')
            context_parts.append(f"Defeated {creature_name} {location}")
        
        return f"Previous adventures: {'; '.join(context_parts)}"
    
    def _generate_fallback_completion_story(self, player: Dict[str, Any], quest: Dict[str, Any]) -> str:
        """Generate a fallback story if AI fails"""
        creature_name = quest['target']['name']
        location = quest['location']
        
        fallback_stories = [
            f"After a fierce battle, {player['name']} emerged victorious against the {creature_name}. "
            f"The ancient beast fell {location}, and peace was restored to the area. "
            f"The villagers cheered as their hero returned, though questions remain about why these creatures have returned.",
            
            f"With skill and determination, {player['name']} tracked down the {creature_name} {location}. "
            f"The confrontation was intense, but the {player['class']}'s training proved decisive. "
            f"Another threat to the kingdom has been eliminated, but the mystery deepens.",
            
            f"The {creature_name} was a formidable opponent, but {player['name']} prevailed through courage and strategy. "
            f"As the dust settled {location}, the kingdom grew a little safer. "
            f"Yet whispers speak of more ancient creatures stirring in the shadows."
        ]
        
        return random.choice(fallback_stories)
    
    def _generate_fallback_encounter_story(self, location: str) -> str:
        """Generate a fallback encounter story if AI fails"""
        fallback_encounters = [
            f"The air grows thick with an ancient presence as you approach {location}. "
            f"Strange tracks mark the ground, and an otherworldly silence hangs in the air.",
            
            f"Your instincts tell you that something powerful has passed through {location} recently. "
            f"The very atmosphere seems charged with primordial energy.",
            
            f"As you survey {location}, you notice signs of disturbance - broken trees, deep gouges in the earth. "
            f"Whatever creature left these marks is unlike anything from the modern world."
        ]
        
        return random.choice(fallback_encounters)

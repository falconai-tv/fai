import os
import logging
from core.brain import Brain
from core.router import Router
from core.memory import save_interaction
from core.processor import process_response
from engines.library_engine import LibraryEngine

logger = logging.getLogger("FalconAI.Agent")

class Agent:
    def __init__(self, music_engine=None, web_engine=None, weather_engine=None, sports_engine=None, library_engine=None):
        self.brain = Brain()
        self.library_engine = library_engine if library_engine else LibraryEngine()
        self.web_engine = web_engine
        self.router = Router(
            web_engine=self.web_engine, 
            library_engine=self.library_engine, 
            music_engine=music_engine, 
            weather_engine=weather_engine, 
            sports_engine=sports_engine
        )

    def handle_request(self, user_input: str) -> dict:
        if not user_input or not user_input.strip():
            return {
                "text": "Please provide a valid instruction.",
                "voice": "Please provide a valid instruction.",
                "meta": {"type": "fallback"}
            }

        cleaned = user_input.strip().lower()

        greetings = ["hello", "hi", "hey", "përshëndetje", "ckemi", "si je", "how are you", "who are you", "kush je ti"]
        if any(g == cleaned or g in cleaned for g in greetings) and len(cleaned) < 25:
            return {
                "text": "Hello! I am FalconAI, your advanced AI assistant and system companion. How can I help you today?",
                "voice": "Hello! I am FalconAI, your advanced AI assistant.",
                "meta": {"type": "chat", "intent": "greeting"}
            }

        music_triggers = ["play", "këngë", "song", "music", "lësho"]
        if any(trig in cleaned for trig in music_triggers) and self.router.music_engine:
            try:
                music_result = self.router.music_engine.play(user_input)
                if isinstance(music_result, dict):
                    return music_result
            except Exception:
                pass
            return {
                "text": f"Playing music for: {user_input}",
                "voice": "Playing music.",
                "meta": {"type": "music", "intent": "play_music"}
            }

        web_triggers = ["what happened", "news", "lajme", "current", "right now", "sot", "kujt", "who is", "what is"]
        if any(trig in cleaned for trig in ["what happened", "news", "lajme", "right now"]) and self.web_engine:
            web_result = self.web_engine.search(user_input)
            if web_result:
                return web_result

        tech_topics = ["kotlin", "java", "python", "clean code", "architecture", "cryptography"]
        if any(topic in cleaned for topic in tech_topics):
            learned_knowledge = self.library_engine.learn_and_extract(cleaned)
            if learned_knowledge:
                return {
                    "text": learned_knowledge,
                    "voice": "Here is what I have learned from your library.",
                    "meta": {"type": "learned_knowledge", "intent": "library_mastery"}
                }

        try:
            brain_output = self.brain.process(user_id="default", text=user_input, router=self.router)
            
            if isinstance(brain_output, dict) and "result" in brain_output:
                raw_result = brain_output["result"]
            else:
                raw_result = {"text": str(brain_output), "voice": str(brain_output)}

            save_interaction(query=user_input, intent="general", meta={})
            return process_response(raw_result)

        except Exception as e:
            logger.error(f"Critical error inside Agent execution pipeline: {e}")
            return {
                "text": "An unexpected error occurred while processing your request.",
                "voice": "An unexpected error occurred.",
                "meta": {"type": "error"}
            }

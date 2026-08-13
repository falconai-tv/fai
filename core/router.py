import os

class Router:
    def __init__(self, web_engine=None, library_engine=None, music_engine=None, weather_engine=None, sports_engine=None, **kwargs):
        self.web_engine = web_engine
        self.library_engine = library_engine
        self.music_engine = music_engine
        self.weather_engine = weather_engine
        self.sports_engine = sports_engine

    def route(self, text: str, intent: str = None, confidence: float = None, **kwargs) -> dict:
        if not text or not text.strip():
            return {
                "text": "Ju lutem shkruani diçka që të mund t'ju ndihmoj.",
                "voice": "Ju lutem shkruani diçka që të mund t'ju ndihmoj.",
                "meta": {"type": "error", "intent": "empty"}
            }

        cleaned = text.strip().lower()

        greetings = ["hello", "hi", "hey", "përshëndetje", "ckemi", "si je", "how are you", "who are you", "kush je ti", "hello, how are you?"]
        if any(g in cleaned for g in greetings):
            response_text = "Hello! I am FalconAI, your advanced AI assistant. How can I help you today?"
            return {
                "text": response_text,
                "voice": response_text,
                "meta": {"type": "chat", "intent": "greeting"}
            }

        if "weather" in cleaned or "moti" in cleaned:
            return {
                "text": "Weather functionality is loading. Please check back shortly.",
                "voice": "Weather functionality is loading.",
                "meta": {"type": "weather", "intent": "weather_query"}
            }

        music_triggers = ["play", "këngë", "song", "music", "lësho"]
        if any(trig in cleaned for trig in music_triggers):
            if self.music_engine and hasattr(self.music_engine, "play"):
                try:
                    music_result = self.music_engine.play(text)
                    if isinstance(music_result, dict):
                        return music_result
                except Exception:
                    pass
            return {
                "text": f"Playing music for: {text}",
                "voice": "Playing music.",
                "meta": {"type": "music", "intent": "play_music"}
            }

        try:
            if self.web_engine and hasattr(self.web_engine, "process"):
                result = self.web_engine.process(text, intent=intent or "general_search")
                if isinstance(result, dict) and result.get("text"):
                    return result
        except Exception:
            pass

        return {
            "text": f"I processed your query: '{text}', but no external matches were found.",
            "voice": "No external matches were found.",
            "meta": {"type": "fallback", "intent": intent}
        }

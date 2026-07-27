import logging
import time
import re

logger = logging.getLogger("FalconAI.Router")

class Router:
    def __init__(self, music_engine, web_engine, weather_engine, sports_engine):
        self.music_engine   = music_engine
        self.web_engine     = web_engine
        self.weather_engine = weather_engine
        self.sports_engine  = sports_engine

        self.MUSIC_INTENTS  = {"music_sad", "music_happy", "music_focus"}
        self.STATIC_INTENTS = {"greeting", "goodbye"}
        self.STATIC_RESPONSES = {
            "greeting": "Hello! I'm FalconAI. How can I help you discover something today?",
            "goodbye":  "Goodbye! I'll be here whenever you need more music or movies."
        }

    def route(self, user_input, intent="unknown", confidence=0.0):
        start_time = time.time()
        cleaned = self.clean_input(user_input)

        # 1. Kontrollo për filma
        if any(w in cleaned for w in ["play movie", "watch movie", "film", "movie", "tubi"]):
            intent = "watch_movie"
            confidence = 1.0

        # 2. Kontrollo për sporte
        elif any(w in cleaned for w in [
            "match", "score", "goal", "premier league", "champions league", 
            "nba", "football", "soccer", "live score", "world cup", "real madrid", "barcelona"
        ]):
            intent = "sports_analysis"
            confidence = 1.0

        # 3. Kontrollo për motin
        elif any(w in cleaned for w in ["weather", "temperature", "forecast", "rain", "snow"]):
            intent = "weather_query"
            confidence = 1.0

        # 4. Çdo gjë tjetër (emra këngëtarësh, zhanre, emocione, ose kërkesa të lira) trajtohet si MUZIKË!
        else:
            intent = "music_happy"
            confidence = 1.0

        try:
            if intent in self.MUSIC_INTENTS or intent == "music_happy":
                result = self.music_engine.process(user_input)
                route_name = "music"
            elif intent == "watch_movie":
                result = self.web_engine.process(cleaned, intent="watch_movie")
                route_name = "web_movie"
            elif intent == "weather_query":
                result = self.weather_engine.process(cleaned)
                route_name = "weather"
            elif intent in ("sports_analysis", "sports_news"):
                result = self.sports_engine.process(cleaned)
                route_name = "sports"
            else:
                result = self.music_engine.process(user_input)
                route_name = "music"

        except Exception as e:
            logger.error(f"Critical exception captured inside routing pipeline: {e}")
            result = self.static_response("I'm having trouble connecting right now. Check your Wi-Fi!")
            route_name = "error"

        if not isinstance(result, dict):
            result = {"type": "fallback", "data": {"text": str(result)}}
        elif "type" not in result:
            result["type"] = "fallback"

        latency = round(time.time() - start_time, 4)
        self.debug_pipeline(user_input, cleaned, intent, confidence, route_name, latency)

        return result

    def clean_input(self, text):
        text = text.lower().strip()
        replacements = {
            "im ":     "i am ",
            "i'm ":    "i am ",
            "whats":   "what is",
            "wanna":   "want to",
            "focused": "focus",
            "pl":      "premier league",
            "ucl":     "champions league",
            "el":      "europa league",
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    def static_response(self, text):
        return {"type": "text", "data": {"text": text}}

    def debug_pipeline(self, original, cleaned, intent, confidence, route, latency):
        print(f"\n--- FALCONAI DEBUG ---")
        print(f"Input:      {original}")
        print(f"Clean:      {cleaned}")
        print(f"Intent:     {intent} ({confidence})")
        print(f"Route:      {route} | Latency: {latency}s")
        print(f"----------------------\n")

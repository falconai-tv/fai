import logging
import time
import re

logger = logging.getLogger("FalconAI.Router")

class Router:
    def __init__(self, music_engine, web_engine, weather_engine):
        self.music_engine = music_engine
        self.web_engine = web_engine
        self.weather_engine = weather_engine

        self.keyword_map = {
            "music_sad":     ["sad", "depressed", "lonely", "heartbreak", "cry", "grief", "miserable", "down", "upset", "broken", "hurt", "pain", "crying", "merzi"],
            "music_happy":   ["happy", "excited", "party", "celebrate", "great", "amazing", "fantastic", "dance", "joy", "fun", "pumped", "energetic", "gezuar"],
            "music_focus":   ["focus", "study", "concentrate", "work", "coding", "productive", "lofi", "ambient", "homework", "reading", "focused", "mesim"],
            "business_news": ["stock", "market", "bitcoin", "crypto", "economy", "shares", "trading", "finance", "inflation", "gold price"],
            "tech_news":     ["tech", "ai", "iphone", "google", "apple", "software", "hardware", "robot", "startup", "microsoft", "tesla", "spacex"],
            "sports_news":   ["sport", "football", "basketball", "nba", "soccer", "tennis", "formula", "league", "match", "score"],
            "watch_war":     ["war", "conflict", "ukraine", "iran", "missile", "military", "attack", "nato", "russia", "israel", "gaza", "bomb"],
            "watch_balkan_news": ["albania", "kosovo", "serbia", "balkan", "tirana", "pristina", "shqiperi", "kosova"],
            "weather_query": ["weather", "rain", "temperature", "forecast", "sunny", "snow", "wind", "moti", "temp"],
            "person_search": ["elon", "musk", "trump", "biden", "zuckerberg", "bezos", "president", "ceo"],
            "watch_movie":   ["movie", "film", "shiko", "play", "tubi", "pluto", "cinema", "watch", "me gjej nje film"],
            "greeting":      ["hello", "hi", "hey", "morning", "evening", "afternoon", "pershendetje", "tung"],
            "goodbye":       ["bye", "goodbye", "farewell", "see you later", "naten", "mira u pafshim"],
        }

        self.intent_category_map = {
            "watch_news": "world",
            "watch_war": "war",
            "watch_balkan_news": "balkan",
            "tech_news": "technology",
            "sports_news": "sports",
            "business_news": "business",
            "weather_query": "general",
            "watch_movie": "vod"
        }

        self.MUSIC_INTENTS    = {"music_sad", "music_happy", "music_focus"}
        self.STATIC_INTENTS   = {"greeting", "goodbye"}
        self.STATIC_RESPONSES = {
            "greeting": "Hello! I'm FalconAI. How can I help you discover something today?",
            "goodbye":  "Goodbye! I'll be here whenever you need more music or movies."
        }

    def route(self, user_input, intent="unknown", confidence=0.0):
        start_time = time.time()
        cleaned = self.clean_input(user_input)

        if any(w in cleaned for w in ["play movie", "watch movie", "shiko filmin", "film", "movie", "tubi"]):
            intent = "watch_movie"
            confidence = 1.0

        else:
            music_intent = self.detect_music(cleaned)
            if music_intent:
                intent = music_intent
                confidence = 1.0

        if intent == "unknown" and any(w in cleaned for w in ["weather", "temperature", "forecast", "moti"]):
            intent = "weather_query"
            confidence = 1.0

        if intent == "unknown" or confidence < 0.7:
            keyword_intent = self.keyword_fallback(cleaned)
            if keyword_intent:
                intent = keyword_intent
                confidence = 0.9

        if intent == "unknown" and any(w in cleaned for w in ["hello", "hi", "hey", "pershendetje"]):
            intent = "greeting"
            confidence = 1.0

        logger.info(f"[ROUTER] Final Intent: {intent} ({confidence})")

        try:
            if intent in self.MUSIC_INTENTS:
                result = self.music_engine.process(cleaned)
                route_name = "music"

            elif intent in self.STATIC_INTENTS:
                result = self.static_response(self.STATIC_RESPONSES.get(intent, "I'm here to help!"))
                route_name = "text"

            elif intent == "watch_movie":
                result = self.web_engine.process(cleaned, intent="watch_movie")
                route_name = "web_movie"

            elif intent == "weather_query":
                result = self.weather_engine.process(cleaned)
                route_name = "weather"

            elif intent == "watch_news":
                channel_result = self.try_channel_match(cleaned)
                if channel_result:
                    result = channel_result
                    route_name = "channel"
                else:
                    result = self.web_engine.process(cleaned, intent="watch_news")
                    route_name = "web"

            elif "i am" in cleaned or "feel" in cleaned:
                result = self.static_response("I'm built to keep you focused. Would you like some lofi music?")
                route_name = "text"

            else:
                result = self.web_engine.process(cleaned, intent="watch_news")
                route_name = "web"

        except Exception as e:
            logger.error(f"Error in routing: {e}")
            result = self.static_response("I'm having trouble connecting to my brain right now. Check your Wi-Fi!")
            route_name = "error"

        latency = round(time.time() - start_time, 4)
        self.debug_pipeline(user_input, cleaned, intent, confidence, route_name, latency)

        return result

    def detect_music(self, text):
        if "focus" in text or "studying" in text or "coding" in text: return "music_focus"
        if "sad" in text or "merzi" in text or "cry" in text: return "music_sad"
        if "happ" in text or "party" in text or "dance" in text: return "music_happy"
        return None

    def keyword_fallback(self, text):
        best_intent = None
        best_score  = 0
        for intent, keywords in self.keyword_map.items():
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                best_score = score
                best_intent = intent
        return best_intent if best_score > 0 else None

    def clean_input(self, text):
        text = text.lower().strip()
        replacements = {
            "im ": "i am ", 
            "i'm ": "i am ", 
            "whats": "what is", 
            "wanna": "want to",
            "focused": "focus"
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    def static_response(self, text):
        return {"type": "text", "data": {"text": text}}

    def try_channel_match(self, text):
        try:
            from core.channel_registry import CHANNELS
            keywords_map = {
                "iran": ["iran", "middle east"],
                "germany": ["germany", "berlin"],
                "ukraine": ["ukraine", "russia"],
                "sports": ["football", "soccer", "nba"]
            }
            for topic, kws in keywords_map.items():
                if any(kw in text for kw in kws):
                    for ch in CHANNELS:
                        if topic in ch.name.lower():
                            return {"type": "channel", "data": {"channel": ch.name, "url": ch.url}}
        except ImportError:
            return None
        return None

    def debug_pipeline(self, original, cleaned, intent, confidence, route, latency):
        print(f"\n--- FALCONAI DEBUG ---")
        print(f"Input: {original}")
        print(f"Clean: {cleaned}")
        print(f"Intent: {intent} ({confidence})")
        print(f"Route: {route} | Latency: {latency}s")
        print(f"----------------------\n")

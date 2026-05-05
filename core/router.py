import logging
import time

logger = logging.getLogger("FalconAI.Router")

class Router:
    def __init__(self, music_engine, web_engine, weather_engine):
        self.music_engine = music_engine
        self.web_engine = web_engine
        self.weather_engine = weather_engine

        self.keyword_map = {
            "music_sad":     ["sad", "depressed", "lonely", "heartbreak", "cry", "grief", "miserable", "down", "upset", "broken", "hurt", "pain", "crying"],
            "music_happy":   ["happy", "excited", "party", "celebrate", "great", "amazing", "fantastic", "dance", "joy", "fun", "pumped", "energetic"],
            "music_focus":   ["focus", "study", "concentrate", "work", "coding", "productive", "lofi", "ambient", "homework", "reading", "focused"],
            "business_news": ["stock", "market", "bitcoin", "crypto", "economy", "nasdaq", "dow", "shares", "trading", "finance", "inflation", "wall street", "s&p", "forex", "currency", "gold price", "oil price"],
            "tech_news":     ["tech", "ai", "iphone", "google", "apple", "software", "hardware", "robot", "startup", "silicon", "microsoft", "tesla", "spacex", "cybersecurity", "gadget", "android"],
            "sports_news":   ["sport", "football", "basketball", "nba", "nfl", "soccer", "tennis", "formula", "cricket", "rugby", "boxing", "mma", "golf", "league", "championship", "match", "score"],
            "watch_war":     ["war", "conflict", "ukraine", "iran", "missile", "military", "attack", "nato", "russia", "israel", "gaza", "bomb", "troops", "invasion"],
            "watch_balkan_news": ["albania", "kosovo", "serbia", "balkan", "tirana", "pristina", "belgrade", "macedonia", "bosnia", "shqiperi", "kosova"],
            "weather_query": ["weather", "rain", "temperature", "forecast", "sunny", "snow", "wind", "humidity", "cold", "hot", "umbrella"],
            "person_search": ["elon", "musk", "trump", "biden", "zuckerberg", "bezos", "obama", "president", "prime minister", "ceo", "celebrity"],
            "greeting":      ["hello", "hi", "hey", "morning", "evening", "afternoon", "howdy", "sup", "greetings"],
            "goodbye":       ["bye", "goodbye", "farewell", "see you later", "take care", "signing off", "i have to go", "gotta go"],
        }

        self.intent_category_map = {
            "watch_news": "world",
            "watch_war": "war",
            "watch_balkan_news": "balkan",
            "watch_channel": "general",
            "tech_news": "technology",
            "sports_news": "sports",
            "person_search": "world",
            "business_news": "business",
            "weather_query": "general",
        }

        self.MUSIC_INTENTS    = {"music_sad", "music_happy", "music_focus"}
        self.STATIC_INTENTS   = {"greeting", "goodbye"}
        self.STATIC_RESPONSES = {
            "greeting": "Hello! How can I help you today?",
            "goodbye":  "Goodbye! See you next time."
        }

    def route(self, user_input, intent="unknown", confidence=0.0):
        start_time = time.time()
        cleaned = self.clean_input(user_input)

        if any(w in cleaned for w in ["hello", "hi ", "hey", "good morning", "good evening", "how are you"]):
            if not any(w in cleaned for w in ["news", "war", "stock", "weather"]):
                intent = "greeting"
                confidence = 1.0

        if any(w in cleaned for w in ["weather", "temperature", "forecast", "rain", "snow", "cold", "hot", "umbrella", "wind", "humid"]):
            intent = "weather_query"
            confidence = 1.0

        music_intent = self.detect_music(cleaned)
        if music_intent:
            intent = music_intent
            confidence = 1.0

        elif confidence < 0.75 or intent in ("unknown", "watch_news"):
            keyword_intent = self.keyword_fallback(cleaned)
            if keyword_intent:
                logger.info(f"[ROUTER] Keyword override: {intent} -> {keyword_intent}")
                intent = keyword_intent

        if intent in ("unknown", "watch_news"):
            intent = "watch_news"

        logger.info(f"[ROUTER] Final Intent: {intent} ({confidence})")

        if intent in self.MUSIC_INTENTS:
            result = self.music_engine.process(cleaned)
            route_name = "music"

        elif intent in self.STATIC_INTENTS:
            result = self.static_response(self.STATIC_RESPONSES[intent])
            route_name = "text"
        
        elif intent == "watch_news":
            channel_result = self.try_channel_match(cleaned)
            
            if channel_result:
                result = channel_result
                route_name = "channel"
                
            else:
                result = self.web_engine.process(cleaned, intent="watch_news")
                route_name = "web"

        elif intent == "watch_channel":
            result = self.web_engine.process(cleaned, intent=intent)
            route_name = "channel"
        
        elif intent == "weather_query":
            result = self.weather_engine.process(cleaned)
            route_name = "weather"

        elif intent in self.intent_category_map:
            result = self.web_engine.process(cleaned, intent=intent)
            route_name = "web"

        else:
            result = self.web_engine.process(cleaned, intent="watch_news")
            route_name = "web"

        latency = round(time.time() - start_time, 4)
        self.debug_pipeline(user_input, cleaned, intent, confidence, route_name, latency)

        return result

    def detect_music(self, text):
        sad_words   = [
            "sad", "depressed", "lonely", "heartbreak", "cry", "crying",
            "grief", "miserable", "upset", "broken", "hurt", "i am down",
            "feeling down", "feel down", "i feel depressed", "i am depressed",
            "not feeling good", "feel bad", "i am not okay", "feel empty"
        ]
        happy_words = [
            "happy", "excited", "party", "celebrate", "amazing", "fantastic",
            "dance", "joy", "pumped", "energetic", "i feel great", "great mood",
            "good mood", "feeling great", "i am happy"
        ]
        focus_words = [
            "focus", "study", "concentrate", "lofi", "ambient", "homework",
            "i am focused", "very focused", "need to focus", "music for work",
            "coding music", "i want to focus", "studying", "i am working"
        ]

        if any(w in text for w in sad_words):
            return "music_sad"
        if any(w in text for w in happy_words):
            return "music_happy"
        if any(w in text for w in focus_words):
            return "music_focus"

        return None

    def keyword_fallback(self, text):
        text = text.lower()
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
            "im ":      "i am ",
            "i'm ":     "i am ",
            "whats":    "what is",
            "happend":  "happened",
            "deppress": "depressed",
            "wanna":    "want to",
            "gonna":    "going to"
        }
        for k, v in replacements.items():
            text = text.replace(k, v)
        return text

    def static_response(self, text):
        return {
            "type": "text",
            "data": {"text": text}
        }

    def fallback(self, text):
        return {
            "type": "text",
            "data": {
                "text": "I'm not sure how to help with that yet."
            }
        }

    def debug_pipeline(self, original, cleaned, intent, confidence, route, latency):
        print("\n[DEBUG PIPELINE]")
        print(f"Input: {original}")
        print(f"Cleaned: {cleaned}")
        print(f"Intent: {intent}")
        print(f"Confidence: {confidence}")
        print(f"Route: {route}")
        print(f"Latency: {latency}")
        print("--------------------------\n")

    def try_channel_match(self, text):
        text = text.lower()
        
        keywords_map = {"iran": ["iran", "tehran", "israel iran", "middle east war"],"germany": ["germany", "berlin", "deutschland"],"ukraine": ["ukraine", "russia", "kyiv", "moscow"],"sports": ["football", "nba", "soccer", "match"],}
        
        from core.channel_registry import CHANNELS
        
        for topic, kws in keywords_map.items():
            if any(kw in text for kw in kws):
                for ch in CHANNELS:
                    if topic in ch.name.lower():
                        return {
                            "type": "channel",
                            "data": {
                                "channel": ch.name,
                                "url": ch.url
                            }
                        }
                    
        return None
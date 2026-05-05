import json
import re
from difflib import SequenceMatcher

def load_channels():
    try:
        with open("data/channels.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


CHANNELS = load_channels()

def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return text.strip()

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

CHANNEL_KEYWORDS = {
    "news": ["news", "lajme", "breaking", "bbc", "cnn", "dw"],
    "sports": ["sport", "football", "tennis", "match", "live"],
    "music": ["music", "radio", "songs", "muzik"],
    "kids": ["kids", "cartoon", "baby"],
    "business": ["finance", "economy", "bloomberg", "money"]
}

def score_channel(query: str, channel_name: str) -> float:
    query = normalize(query)
    name = normalize(channel_name)

    base = similarity(query, name)

    boost = 0.0
    for _, keywords in CHANNEL_KEYWORDS.items():
        for kw in keywords:
            if kw in query and kw in name:
                boost += 0.25

    return base + boost

class ChannelsEngine:
    def process(self, user_input: str, intent_data=None):
        return self.find_channel(user_input)

    def find_channel(self, query: str):
        if not CHANNELS:
            return {
                "type": "channel",
                "status": "empty_db",
                "data": None
            }

        scored = []

        for ch in CHANNELS:
            name = ch.get("name", "")
            url = ch.get("url", "")

            score = score_channel(query, name)

            scored.append({
                "name": name,
                "url": url,
                "score": score
            })

        scored.sort(key=lambda x: x["score"], reverse=True)

        best = scored[0]

        if best["score"] < 0.45:
            return {
                "type": "channel",
                "status": "not_found",
                "query": query,
                "suggestions": scored[:5]
            }

        return {
            "type": "channel",
            "status": "found",
            "data": {
                "name": best["name"],
                "url": best["url"],
                "confidence": round(best["score"], 2),
                "alternatives": scored[1:4]
            }
        }

    def recommend_channels(self, topic: str):
        topic = normalize(topic)

        results = []

        for ch in CHANNELS:
            name = ch.get("name", "")
            score = score_channel(topic, name)

            if score > 0.4:
                results.append({
                    "name": name,
                    "url": ch.get("url"),
                    "score": score
                })

        results.sort(key=lambda x: x["score"], reverse=True)

        return results[:5]
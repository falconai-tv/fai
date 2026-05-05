import json
import os
import time
from collections import Counter, defaultdict
from typing import Dict, Any


class Memory:
    def __init__(self, file_path="data/user_memory.json", max_history=200):
        self.file_path = file_path
        self.max_history = max_history
        self._ensure_file()

    def _ensure_file(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

        if not os.path.exists(self.file_path):
            self._save({
                "history": [],
                "preferences": {},
                "stats": {}
            })

    def _load(self) -> Dict[str, Any]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save(self, data: Dict[str, Any]):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def save_interaction(self, query: str, intent: str, meta: dict = None):
        data = self._load()

        entry = {
            "query": query,
            "intent": intent,
            "timestamp": int(time.time())
        }

        if meta:
            entry["meta"] = meta

        data["history"].append(entry)
        data["history"] = data["history"][-self.max_history:]

        self._update_preferences(data)
        self._save(data)

    def _update_preferences(self, data: Dict[str, Any]):
        history = data["history"]

        intent_counter = Counter()
        keyword_counter = Counter()

        for item in history:
            intent = item.get("intent")
            query = item.get("query", "")

            if intent:
                intent_counter[intent] += 1

            for word in query.lower().split():
                if len(word) > 3:
                    keyword_counter[word] += 1

        data["preferences"] = {
            "top_intents": intent_counter.most_common(5),
            "top_keywords": keyword_counter.most_common(10)
        }

        data["stats"] = {
            "total_queries": len(history),
            "last_updated": int(time.time())
        }

    def get_preferences(self):
        return self._load().get("preferences", {})

    def get_history(self, limit=10):
        return self._load().get("history", [])[-limit:]

    def get_stats(self):
        return self._load().get("stats", {})

    def get_intent_boost(self, query: str):
        prefs = self.get_preferences()

        boosts = defaultdict(float)

        for intent, count in prefs.get("top_intents", []):
            boosts[intent] += count * 0.1

        query_words = query.lower().split()

        for word, count in prefs.get("top_keywords", []):
            if word in query_words:
                boosts["general_search"] += 0.2
                boosts["watch_channel"] += 0.3
                boosts["music_happy"] += 0.15

        return dict(boosts)

    def personalize_text(self, text: str):
        prefs = self.get_preferences()

        top = prefs.get("top_intents", [])
        if not top:
            return text

        main_intent = top[0][0]

        prefixes = {
            "watch_channel": "Based on your viewing habits → ",
            "general_search": "Based on your interests → ",
            "music_happy": "Based on your music taste → "
        }

        return prefixes.get(main_intent, "") + text

    def get_insights(self):
        data = self._load()

        return {
            "total_queries": data.get("stats", {}).get("total_queries", 0),
            "top_intents": data.get("preferences", {}).get("top_intents", []),
            "top_keywords": data.get("preferences", {}).get("top_keywords", [])
        }

_memory_instance = None

def _get_instance():
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = Memory()
    return _memory_instance

def save_interaction(query, intent, meta=None):
    return _get_instance().save_interaction(query, intent, meta)

def get_intent_boost(query):
    return _get_instance().get_intent_boost(query)
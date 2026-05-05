import os
import pickle
import numpy as np
from typing import Dict

MODEL_PATH = os.path.join("ml", "model.pkl")
VECTORIZER_PATH = os.path.join("ml", "vectorizer.pkl")

class FalconPredictor:
    def __init__(self):
        self.model = None
        self.vectorizer = None

        self._load_assets()

    def _load_assets(self):
        try:
            with open(MODEL_PATH, "rb") as f:
                self.model = pickle.load(f)

            with open(VECTORIZER_PATH, "rb") as f:
                self.vectorizer = pickle.load(f)

            print("ML model loaded")

        except Exception as e:
            print("Failed to load model:", e)
            self.model = None
            self.vectorizer = None

    def predict(self, text: str) -> Dict:
        text = text.lower().strip()

        rule = self._rule_based(text)
        if rule:
            return rule

        if self.model and self.vectorizer:
            try:
                X = self.vectorizer.transform([text])
                probs = self.model.predict_proba(X)[0]

                idx = np.argmax(probs)
                confidence = float(probs[idx])
                intent = self.model.classes_[idx]

                if confidence < 0.45:
                    return self._fallback(text, confidence)

                return {
                    "intent": intent,
                    "confidence": round(confidence, 3),
                    "source": "ml"
                }

            except Exception as e:
                print("ML error:", e)
                return self._fallback(text, 0.0)

        return self._fallback(text, 0.0)

    def _rule_based(self, text: str):
        t = text

        if any(w in t for w in ["happy", "great", "good mood", "excited"]):
            return {"intent": "music_happy", "confidence": 0.9, "source": "rule"}

        if any(w in t for w in ["sad", "depressed", "lonely", "bad mood"]):
            return {"intent": "music_sad", "confidence": 0.9, "source": "rule"}

        if any(w in t for w in ["focus", "study", "work", "concentrate"]):
            return {"intent": "music_focus", "confidence": 0.85, "source": "rule"}

        if any(w in t for w in ["iran", "war", "ukraine", "usa", "conflict"]):
            return {"intent": "watch_war", "confidence": 0.85, "source": "rule"}

        if "news" in t or "what happened" in t:
            return {"intent": "watch_news", "confidence": 0.8, "source": "rule"}

        if any(w in t for w in ["watch", "channel", "tv", "live"]):
            return {"intent": "watch_channel", "confidence": 0.8, "source": "rule"}

        if any(w in t for w in ["what is", "tell me", "search", "information"]):
            return {"intent": "general_search", "confidence": 0.7, "source": "rule"}

        return None

    def _fallback(self, text: str, confidence: float):
        return {
            "intent": "general_search",
            "confidence": round(confidence, 3),
            "source": "fallback"
        }

_predictor_instance = FalconPredictor()


def predict(text: str) -> Dict:
    return _predictor_instance.predict(text)
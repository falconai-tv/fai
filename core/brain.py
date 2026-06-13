import os
import sys
import logging

logger = logging.getLogger("FalconAI.Brain")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from ml.predict import predict
except ImportError:
    logger.warning("ml.predict module could not be reached via direct pathing. Deploying predictable fallback.")
    def predict(text):
        return {"intent": "unknown", "confidence": 0.0}

class FalconBrain:
    def __init__(self):
        logger.info("FalconBrain initializing and caching ML engine tensor weights...")
        
    def process(self, user_id: str, text: str, router=None) -> dict:
        if not text:
            return {"result": {"type": "fallback", "data": {"text": "No input text provided."}}}

        cleaned_text = text.lower().strip()
        logger.info(f"[BRAIN] Processing input token: '{cleaned_text}' for identity node: {user_id}")

        sports_keywords = ["analyze", "live game", "world cup", "tactics", "match", "football", "formation", "pitch"]
        if any(w in cleaned_text for w in sports_keywords):
            logger.info("[BRAIN] Intent match intercepted: Directing pipeline to Sports Analysis.")
            if router:
                routed_result = router.route(text, intent="sports_analysis", confidence=1.0)
                return {"result": routed_result}

        intent = "unknown"
        confidence = 0.0
        
        try:
            prediction = predict(cleaned_text)
            intent = prediction.get("intent", "unknown")
            confidence = prediction.get("confidence", 0.0)
            logger.info(f"[BRAIN] ML Model Prediction -> Intent: {intent} | Confidence: {confidence}")
        except Exception as e:
            logger.error(f"[BRAIN] Exception intercepted inside ML prediction phase: {e}")

        if router:
            routed_result = router.route(text, intent=intent, confidence=confidence)
            return {"result": routed_result}

        logger.warning("[BRAIN] Router matrix is unavailable. Emitting fallback payload structure.")
        return {
            "result": {
                "type": "fallback",
                "data": {
                    "text": "The intelligent routing engine is currently offline. Please attempt query execution again."
                }
            }
        }

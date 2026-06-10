import time
from typing import Dict, Any

from ml.predict import predict
from core.memory import save_interaction, get_intent_boost

class FalconBrain:
    def __init__(self):
        self.stats = {
            "requests": 0,
            "successful": 0,
            "fallbacks": 0
        }

    def analyze(self, text: str, context: Dict = None) -> Dict[str, Any]:
        try:
            base_prediction = predict(text)
            if not isinstance(base_prediction, dict):
                base_prediction = {"intent": "unknown", "confidence": 0.0, "source": "fallback"}
        except Exception as e:
            print("[Brain Predict Error]", e)
            base_prediction = {"intent": "unknown", "confidence": 0.0, "source": "error_fallback"}

        intent = base_prediction.get("intent", "unknown")
        confidence = base_prediction.get("confidence", 0.0)

        try:
            boost = get_intent_boost(text)
            if isinstance(boost, dict) and intent in boost:
                confidence += boost[intent]
        except Exception as e:
            print("[Brain Boost Error]", e)

        confidence = min(confidence, 1.0)

        return {
            "intent": intent,
            "confidence": round(confidence, 3),
            "source": base_prediction.get("source", "unknown")
        }

    def process(self, user_id: str, text: str, router) -> Dict[str, Any]:
        start_time = time.time()
        self.stats["requests"] += 1

        analysis = self.analyze(text)
        intent = analysis["intent"]
        confidence = analysis["confidence"]

        route_result = router.route(text, intent, confidence)

        if route_result is None:
            route_result = {"type": "fallback", "data": {"text": "I encountered an empty response."}}
        elif not isinstance(route_result, dict):
            route_result = {"type": "fallback", "data": {"text": str(route_result)}}

        try:
            save_interaction(text, intent, {
                "confidence": confidence,
                "engine": route_result.get("type", "unknown")
            })
        except Exception as e:
            print("[Memory Error]", e)

        if route_result.get("type") in ("text", "fallback", "error"):
            self.stats["fallbacks"] += 1
        else:
            self.stats["successful"] += 1

        latency = round(time.time() - start_time, 4)

        return {
            "intent": intent,
            "confidence": confidence,
            "result": route_result,
            "latency": latency
        }

    def debug(self, user_id: str, text: str, router):
        result = self.process(user_id, text, router)
        engine_type = result["result"].get("type") if isinstance(result.get("result"), dict) else "unknown"
        return {
            "input": text,
            "intent": result["intent"],
            "confidence": result["confidence"],
            "engine": engine_type,
            "latency_ms": result["latency"] * 1000,
            "stats": self.stats
        }

    def health(self):
        return {
            "status": "ok",
            "stats": self.stats
        }

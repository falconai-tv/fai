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
        base_prediction = predict(text)

        intent = base_prediction.get("intent", "unknown")
        confidence = base_prediction.get("confidence", 0.0)

        boost = get_intent_boost(text)
        if intent in boost:
            confidence += boost[intent]

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

        # ✅ FIX: parametrat në rend të saktë
        route_result = router.route(text, intent, confidence)

        try:
            save_interaction(text, intent, {
                "confidence": confidence,
                "engine": route_result.get("type")
            })
        except Exception as e:
            print("[Memory Error]", e)

        # ✅ FIX: kontrollo saktë tipin e route_result
        if route_result.get("type") in ("text", "fallback"):
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
        return {
            "input": text,
            "intent": result["intent"],
            "confidence": result["confidence"],
            "engine": result["result"].get("type"),
            "latency_ms": result["latency"] * 1000,
            "stats": self.stats
        }

    def health(self):
        return {
            "status": "ok",
            "stats": self.stats
        }
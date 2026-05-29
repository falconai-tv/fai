import json
import time
import traceback
import os
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS

from core.brain import FalconBrain
from core.router import Router
from engines.web_engine import WebEngine
from engines.music_engine import MusicEngine
from engines.weather_engine import WeatherEngine
from utils.text_cleaner import TextCleaner


# OPTIONAL import (nuk e rrëzon app-in nëse mungon)
try:
    from core.channel_registry import find_best_channel
except Exception:
    find_best_channel = None


app = Flask(__name__)
CORS(app)

cleaner = TextCleaner()

DEBUG = True
LOG_FILE = "data/logs.jsonl"

brain = None
router = None


def log_event(entry):
    try:
        os.makedirs("data", exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print(f"[LOG ERROR] {e}")


def format_response(result):
    if not result:
        return {
            "type": "text",
            "text": "I encountered an error. Please try again."
        }

    if not isinstance(result, dict):
        return {
            "type": "text",
            "text": str(result)
        }

    response_type = result.get("type", "text")
    data = result.get("data", {})

    flat = {"type": response_type}

    if isinstance(data, dict):
        flat.update(data)

    return flat


def init_system():
    global brain, router

    print("Loading FalconAI systems...\n")

    web_engine = WebEngine()
    music_engine = MusicEngine()
    weather_engine = WeatherEngine()

    router = Router(music_engine, web_engine, weather_engine)
    brain = FalconBrain()

    print("All systems ready!\n")


def process_logic(user_input: str):
    start_time = time.time()
    cleaned = cleaner.clean(user_input)

    intent = "unknown"
    confidence = 0.0

    # ---------------------------
    # 1. Optional TV CHANNEL STEP
    # ---------------------------
    channel_route = None

    if find_best_channel:
        try:
            best_channel = find_best_channel(cleaned)

            if best_channel:
                channel_route = {
                    "type": "channel",
                    "data": {
                        "stream_url": best_channel.url,
                        "channel_name": best_channel.name,
                        "status": "success"
                    }
                }

                log_event({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "input": user_input,
                    "cleaned": cleaned,
                    "intent": "watch_tv",
                    "route": "channel",
                    "latency": round(time.time() - start_time, 4)
                })

                return format_response(channel_route)

        except Exception as e:
            print(f"[CHANNEL ERROR] {e}")

    # ---------------------------
    # 2. BRAIN ANALYSIS
    # ---------------------------
    try:
        brain_result = brain.analyze(cleaned)
        intent = brain_result.get("intent", "unknown")
        confidence = brain_result.get("confidence", 0.0)
    except Exception as e:
        print(f"[BRAIN ERROR] {e}")

    # ---------------------------
    # 3. ROUTER
    # ---------------------------
    try:
        route_result = router.route(
            cleaned,
            intent=intent,
            confidence=confidence
        )
    except Exception as e:
        print(f"[ROUTER ERROR] {e}")
        route_result = {
            "type": "text",
            "data": {
                "text": "Service temporarily unavailable."
            }
        }

    # ---------------------------
    # LOGGING
    # ---------------------------
    log_event({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": user_input,
        "cleaned": cleaned,
        "intent": intent,
        "confidence": confidence,
        "route": route_result.get("type"),
        "latency": round(time.time() - start_time, 4)
    })

    return format_response(route_result)


@app.route("/")
def home():
    return "FalconAI API is online."


@app.route("/process", methods=["POST"])
def api_process():
    try:
        data = request.json or {}
        user_input = data.get("text", "").strip()

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        result = process_logic(user_input)
        return jsonify(result)

    except Exception as e:
        if DEBUG:
            traceback.print_exc()

        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    init_system()
    app.run(host="0.0.0.0", port=port, debug=False)

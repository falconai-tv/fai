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

from core.channel_registry import find_best_channel


# =========================
# FLASK APP (IMPORTANT)
# =========================
app = Flask(__name__)
CORS(app)


# =========================
# GLOBALS
# =========================
cleaner = TextCleaner()

brain = None
router = None

DEBUG = True
LOG_FILE = "data/logs.jsonl"


# =========================
# INIT SYSTEM
# =========================
def init_system():
    global brain, router

    print("Starting FalconAI systems...")

    web_engine = WebEngine()
    music_engine = MusicEngine()
    weather_engine = WeatherEngine()

    router = Router(music_engine, web_engine, weather_engine)
    brain = FalconBrain()

    print("System ready.")


# =========================
# LOGGING
# =========================
def log_event(entry):
    try:
        os.makedirs("data", exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print("[LOG ERROR]", e)


# =========================
# CORE LOGIC
# =========================
def process_logic(user_input: str):
    start_time = time.time()

    cleaned = cleaner.clean(user_input)

    # 1. Channel check (TV first)
    try:
        channel = find_best_channel(cleaned)
        if channel:
            return {
                "type": "channel",
                "data": {
                    "stream_url": channel.url,
                    "channel_name": channel.name,
                    "status": "success"
                }
            }
    except Exception as e:
        print("[CHANNEL ERROR]", e)

    # 2. Brain intent
    try:
        brain_result = brain.analyze(cleaned)
        intent = brain_result.get("intent", "unknown")
        confidence = brain_result.get("confidence", 0.0)
    except Exception as e:
        print("[BRAIN ERROR]", e)
        intent, confidence = "unknown", 0.0

    # 3. Router
    try:
        result = router.route(
            cleaned,
            intent=intent,
            confidence=confidence
        )
    except Exception as e:
        print("[ROUTER ERROR]", e)
        result = {
            "type": "text",
            "data": {
                "text": "Service temporarily unavailable."
            }
        }

    # 4. Log
    log_event({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": user_input,
        "cleaned": cleaned,
        "intent": intent,
        "confidence": confidence,
        "latency": round(time.time() - start_time, 4)
    })

    return result


# =========================
# ROUTES
# =========================
@app.route("/")
def home():
    return "FalconAI API is running."


@app.route("/process", methods=["POST"])
def process():
    try:
        data = request.json or {}
        text = data.get("text", "").strip()

        if not text:
            return jsonify({"error": "Empty input"}), 400

        result = process_logic(text)
        return jsonify(result)

    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# =========================
# BOOT
# =========================
print("Booting FalconAI...")
init_system()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)

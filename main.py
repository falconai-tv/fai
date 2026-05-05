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
from utils.voice import speak

app = Flask(__name__)
CORS(app) 

cleaner = TextCleaner()

DEBUG    = True
LOG_FILE = "data/logs.jsonl"

brain  = None
router = None

def log_event(entry):
    try:
        os.makedirs("data", exist_ok=True)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except Exception as e:
        print("[LOG ERROR]", e)

def format_response(result):
    if not isinstance(result, dict):
        return str(result)

    data = result.get("data")
    result_type = result.get("type")

    if isinstance(data, dict):
        voice_text = data.get("voice_text")

        if voice_text and result_type != "music":
            try:
                speak(voice_text)
            except:
                pass

        return data.get("text") or data.get("response") or str(data)

    return str(data or "No response")

def init_system():
    global brain, router

    print("Loading FalconAI systems...\n")

    web_engine     = WebEngine()
    music_engine   = MusicEngine()
    weather_engine = WeatherEngine()

    router = Router(music_engine, web_engine, weather_engine)
    brain  = FalconBrain()

    print("All systems ready!\n")

def process(user_input: str):
    start_time = time.time()

    cleaned_input = cleaner.clean(user_input)

    brain_result = brain.analyze(cleaned_input)
    intent       = brain_result.get("intent", "unknown")
    confidence   = brain_result.get("confidence", 0.0)

    route_result = router.route(
        cleaned_input,
        intent=intent,
        confidence=confidence
    )

    log_event({
        "timestamp":  datetime.now(timezone.utc).isoformat(),
        "input":      user_input,
        "cleaned":    cleaned_input,
        "intent":     intent,
        "confidence": confidence,
        "route":      route_result.get("type"),
        "latency":    round(time.time() - start_time, 4)
    })

    return format_response(route_result)

def print_banner():
    print("""
    ███████╗ █████╗ ██╗      ██████╗ ██████╗ ███╗   ██╗ █████╗ ██╗
    ██╔════╝██╔══██╗██║     ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██║
    █████╗  ███████║██║     ██║     ██║   ██║██╔██╗ ██║███████║██║
    ██╔══╝  ██╔══██║██║     ██║     ██║   ██║██║╚██╗██║██╔══██║██║
    ██║     ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║  ██║██║
    ╚═╝     ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝
                    V2 — Powered by FalconAI
    """)

print_banner()
init_system()

@app.route('/')
def home():
    return "FalconAI API is online."

@app.route('/process', methods=['POST'])
def api_process():
    try:
        data = request.json
        user_input = data.get("text", "").strip()

        if not user_input:
            return jsonify({"error": "No input provided"}), 400

        response = process(user_input)
        
        return jsonify({
            "falcon_ai": response
        })

    except Exception as e:
        if DEBUG:
            traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
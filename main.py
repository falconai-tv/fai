import os
import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

# Sigurohemi që folderi root është në path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from core.brain import FalconBrain
from core.router import Router
from engines.web_engine import WebEngine
from engines.music_engine import MusicEngine
from engines.weather_engine import WeatherEngine
from engines.channels_engine import ChannelsEngine

app = Flask(__name__)
CORS(app)

# Variablat globale të inicializuara si None
router = None
brain = None

def boot_system():
    global router, brain
    print("--- FalconAI: Starting Boot Sequence ---")
    
    try:
        # Inicializojmë motorët një nga një për të kapur fajtorin
        print("Initializing engines...")
        w_engine = WebEngine()
        m_engine = MusicEngine()
        we_engine = WeatherEngine()
        c_engine = ChannelsEngine()
        
        # Inicializojmë Router-in
        router = Router(
            music_engine=m_engine, 
            web_engine=w_engine, 
            weather_engine=we_engine, 
            channels_engine=c_engine
        )
        print("✅ Router & Engines: READY")
        
    except Exception as e:
        print("❌ CRITICAL ERROR during Engine initialization:")
        traceback.print_exc() # Kjo do të tregojë rreshtin fiks pse dështon

    try:
        print("Loading ML Brain...")
        brain = FalconBrain()
        print("✅ ML Brain: READY")
    except Exception as e:
        print(f"⚠️ Warning: Brain failed to load: {e}")

# Ekzekutojmë boot-in përpara se Flask të nisin
boot_system()

def heuristic_layer(text):
    t = text.lower().strip()
    if any(word in t for word in ["weather", "moti", "tirana", "forecast"]):
        return {"intent": "get_weather", "entities": {"location": text}, "confidence": 1.0}
    if any(word in t for word in ["play", "luaj", "music", "kenga"]):
        return {"intent": "play_music", "entities": {"query": text}, "confidence": 1.0}
    return None

@app.route('/')
def index():
    status = "online" if router else "partial_error"
    return jsonify({"status": status, "system": "FalconAI", "version": "2.1.5"}), 200

@app.route('/process', methods=['POST'])
def process_request():
    global router, brain
    
    # Siguria e fundit: Nëse router dështoi në boot, provo inicializim emergjent
    if router is None:
        return jsonify({
            "status": "error", 
            "message": "Router not initialized. Check server logs for boot errors."
        }), 500

    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400
        
        user_text = data['text']
        
        # 1. Heuristics
        intent_data = heuristic_layer(user_text)
        
        # 2. Brain
        if not intent_data:
            if brain:
                intent_data = brain.process(user_text)
            else:
                intent_data = {"intent": "web_search", "entities": {"query": user_text}, "confidence": 0.5}

        # 3. Route
        response = router.route(intent_data)
        
        if 'status' not in response:
            response['status'] = 'success'
            
        return jsonify(response), 200

    except Exception as e:
        traceback.print_exc()
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

import os
import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

# Shtohet rruga për importet e moduleve core dhe engines
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.brain import FalconBrain
from core.router import Router
from engines.web_engine import WebEngine
from engines.music_engine import MusicEngine
from engines.weather_engine import WeatherEngine
from engines.channels_engine import ChannelsEngine

app = Flask(__name__)
CORS(app)

print("--- FalconAI: Booting System ---")

# --- Inicializimi Global ---
# I nxjerrim jashtë try/except që të jemi sigurt që 'router' ekziston gjithmonë
try:
    web_engine = WebEngine()
    music_engine = MusicEngine()
    weather_engine = WeatherEngine()
    channels_engine = ChannelsEngine()

    router = Router(
        music_engine=music_engine, 
        web_engine=web_engine, 
        weather_engine=weather_engine, 
        channels_engine=channels_engine
    )
    print("--- Router & Engines: Ready ---")
except Exception as e:
    print(f"CRITICAL ERROR INITIALIZING ENGINES: {str(e)}")
    traceback.print_exc()
    router = None

# Brain kërkon ngarkim modeli ML, ndaj e trajtojmë me kujdes
try:
    brain = FalconBrain()
    print("--- ML Brain: Loaded ---")
except Exception as e:
    print(f"WARNING: Brain could not load: {str(e)}")
    brain = None

def heuristic_layer(text):
    """
    Korigjon gabimet e klasifikimit përpara se të shkojnë te AI.
    Zgjidhja për rastet si 'weather in Tirana'.
    """
    t = text.lower().strip()
    
    # Weather keywords
    if any(word in t for word in ["weather", "moti", "temperatura", "forecast"]):
        return {
            "intent": "get_weather", 
            "entities": {"location": text}, 
            "confidence": 1.0,
            "method": "heuristic"
        }
    
    # Music keywords
    if any(word in t for word in ["play", "luaj", "muzik", "music", "kenga"]):
        return {
            "intent": "play_music", 
            "entities": {"query": text}, 
            "confidence": 1.0,
            "method": "heuristic"
        }

    return None

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "system": "FalconAI",
        "version": "2.1.2",
        "erind_mode": True
    }), 200

@app.route('/process', methods=['POST'])
def process_request():
    # Sigurohemi që Flask i sheh variablat globale
    global router, brain

    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400
        
        user_text = data['text']
        print(f"Input: {user_text}")

        # Kontrolli 1: Heuristics (Prioritet mbi AI)
        intent_data = heuristic_layer(user_text)

        # Kontrolli 2: ML Brain (Nëse Heuristics nuk gjen gjë)
        if not intent_data:
            if brain:
                intent_data = brain.process(user_text)
                intent_data["method"] = "ml_brain"
            else:
                # Fallback nëse modeli nuk është ngarkuar
                intent_data = {"intent": "web_search", "entities": {"query": user_text}, "confidence": 0.5}

        # Kontrolli 3: Ekzekutimi via Router
        if router:
            response = router.route(intent_data)
        else:
            return jsonify({"status": "error", "message": "Router not initialized"}), 500

        # Shtojmë info për debug në Android Logcat
        if 'status' not in response:
            response['status'] = 'success'
        
        response['debug_intent'] = intent_data.get('intent')
        response['debug_method'] = intent_data.get('method')
            
        return jsonify(response), 200

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        traceback.print_exc()
        return jsonify({
            "status": "error", 
            "message": "Internal processing error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    # Railway përdor variablën PORT
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

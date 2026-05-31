import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Sigurohemi që folderi root është në path për importet e core/engines
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.brain import FalconBrain
from core.router import Router
from engines.web_engine import WebEngine
from engines.music_engine import MusicEngine
from engines.weather_engine import WeatherEngine
from engines.channels_engine import ChannelsEngine

app = Flask(__name__)
CORS(app)

print("--- FalconAI Booting ---")

# Inicializimi i sistemeve
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

    brain = FalconBrain()
    
    print("--- All Systems Ready (ML Model Loaded) ---")
except Exception as e:
    print(f"FATAL ERROR DURING BOOT: {str(e)}")

def heuristic_layer(text):
    """
    Ky funksion kap fjalët kyçe përpara se të shkojnë në ML Brain.
    Nëse gjen një ndeshje të qartë, kthen intentin direkt.
    """
    t = text.lower().strip()
    
    # 1. Weather Bypass (Zgjidhja për problemin në Logcat)
    if any(word in t for word in ["weather", "moti", "temperatura", "forecast", "tirana", "prishtina"]):
        return {
            "intent": "get_weather", 
            "entities": {"location": text}, 
            "confidence": 1.0,
            "source": "heuristic"
        }
    
    # 2. News Bypass
    if any(word in t for word in ["news", "lajme", "lajmet", "top channel", "klan"]):
        return {
            "intent": "get_news", 
            "confidence": 1.0,
            "source": "heuristic"
        }
    
    # 3. Music/YouTube Bypass
    if any(word in t for word in ["luaj", "play", "kenga", "muzik", "music", "spotify", "youtube"]):
        return {
            "intent": "play_music", 
            "entities": {"query": text}, 
            "confidence": 0.9,
            "source": "heuristic"
        }

    return None

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "system": "FalconAI",
        "version": "2.1.0",
        "author": "Erind Musliu"
    }), 200

@app.route('/process', methods=['POST'])
def process_request():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400
        
        user_text = data['text']
        print(f"\n[USER INPUT]: {user_text}")

        # Hapi 1: Kontrolli Heuristik (Mbrojtja nga gabimet e modelit)
        intent_data = heuristic_layer(user_text)

        # Hapi 2: Nëse Heuristics nuk gjen gjë, përdorim ML Brain
        if not intent_data:
            intent_data = brain.process(user_text)
            print(f"[ML BRAIN]: Intent detected -> {intent_data.get('intent')}")
        else:
            print(f"[HEURISTIC]: Intent forced -> {intent_data.get('intent')}")

        # Hapi 3: Routing te engine përkatës
        response = router.route(intent_data)

        # Hapi 4: Formatimi i fundit i përgjigjes
        if 'status' not in response:
            response['status'] = 'success'
        
        # Shtojmë meta-data për debug në Android
        response['intent'] = intent_data.get('intent')
        response['confidence'] = intent_data.get('confidence', 0.0)
            
        return jsonify(response), 200

    except Exception as e:
        print(f"!!! PROCESSING ERROR: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": "Internal processing error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    # Përdorimi i portit nga variablat e ambientit (Railway/Heroku)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

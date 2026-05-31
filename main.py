import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Sigurohemi që folderi rrënjë është në path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Inicializojmë variablat globalë
brain = None
router = None

def init_all():
    global brain, router
    try:
        print("--- Duke nisur inicializimin e motorëve... ---")
        
        # Importet brenda funksionit për të kapur gabimet specifike
        from engines.web_engine import WebEngine
        from engines.music_engine import MusicEngine
        from engines.weather_engine import WeatherEngine
        from engines.channels_engine import ChannelsEngine
        from core.router import Router
        from core.brain import FalconBrain

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
        
        print("--- Duke ngarkuar FalconBrain (ML Model)... ---")
        brain = FalconBrain()
        
        print("--- [SUCCESS] FalconAI është gati! ---")
    except Exception as e:
        # KJO DO TË NA TREGOJË GABIMIN E SAKTË TE RAILWAY LOGS
        print(f"--- [ERROR] Dështoi inicializimi: {str(e)} ---")
        import traceback
        traceback.print_exc()

# Thirrim inicializimin menjëherë
init_all()

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "brain_ready": brain is not None,
        "router_ready": router is not None
    }), 200

@app.route('/process', methods=['POST'])
def process_request():
    global brain, router 
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400
        
        user_text = data['text']

        if brain is None:
            return jsonify({
                "status": "error", 
                "message": "Brain is not defined. Kontrollo Railway Logs për gabimin e importit."
            }), 500

        intent_data = brain.process(user_text)
        response = router.route(intent_data)
        
        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "status": "error", 
            "message": "Internal processing error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

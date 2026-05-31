import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

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

@app.route('/')
def index():
    return jsonify({
        "status": "online",
        "system": "FalconAI",
        "version": "2.0.0"
    }), 200

@app.route('/process', methods=['POST'])
def process_request():
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400
        
        user_text = data['text']
        print(f"User Input: {user_text}")

        intent_data = brain.process(user_text)

        response = router.route(intent_data)

        if 'status' not in response:
            response['status'] = 'success'
            
        return jsonify(response), 200

    except Exception as e:
        print(f"Processing Error: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": "Internal processing error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

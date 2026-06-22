import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from core.brain import FalconBrain
from core.router import router
from engines.web_engine import WebEngine
from engines.music_engine import MusicEngine
from engines.weather_engine import WeatherEngine
from engines.sports_engine import SportsEngine

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

print("--- FalconAI Booting ---")

web_engine = None
music_engine = None
weather_engine = None
sports_engine = None
router = None
brain = None

try:
    web_engine = WebEngine()
    music_engine = MusicEngine()
    weather_engine = WeatherEngine()
    sports_engine = SportsEngine()

    router = Router(
        music_engine=music_engine, 
        web_engine=web_engine, 
        weather_engine=weather_engine, 
        sports_engine=sports_engine
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
        "version": "2.1.0"
    }), 200

@app.route('/process', methods=['POST', 'OPTIONS'])
def process_request():
    # Menaxhimi i kërkesës pre-flight të browser-it
    if request.method == 'OPTIONS':
        return jsonify({"status": "ok"}), 200

    try:
        if brain is None or router is None:
            return jsonify({
                "status": "error",
                "message": "FalconBrain is not initialized properly. Check boot logs."
            }), 500

        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400
        
        user_text = data['text']
        user_id = data.get('user_id', "default_user")
        
        print(f"User Input: {user_text}")

        brain_response = brain.process(user_id=user_id, text=user_text, router=router)
        final_response = brain_response.get("result", {})

        if isinstance(final_response, dict) and 'status' not in final_response:
            final_response['status'] = 'success'
            
        return jsonify(final_response), 200

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

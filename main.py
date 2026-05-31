import os
import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

# Shtohet path-i per importet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

brain = None
router = None
startup_error = "Sistemi po inicializohet..."

def init_all():
    global brain, router, startup_error
    try:
        from core.brain import FalconBrain
        from core.router import Router
        from engines.web_engine import WebEngine
        from engines.music_engine import MusicEngine
        from engines.weather_engine import WeatherEngine

        # Inicializimi i motoreve baze
        web_engine = WebEngine()
        music_engine = MusicEngine()
        weather_engine = WeatherEngine()

        # Router-i tani merr vetem 3 argumente
        router = Router(
            music_engine=music_engine, 
            web_engine=web_engine, 
            weather_engine=weather_engine
        )
        
        brain = FalconBrain()
        startup_error = "Success"
        print("--- [SUCCESS] FalconAI Backend is ready ---")

    except Exception as e:
        full_trace = traceback.format_exc()
        startup_error = f"GABIM: {str(e)}\n\n{full_trace}"
        print(f"BOOT ERROR: {startup_error}")

init_all()

@app.route('/')
def health():
    return jsonify({
        "status": "online",
        "brain_ready": brain is not None,
        "error_details": startup_error
    }), 200

@app.route('/process', methods=['POST'])
def process_request():
    global brain, router 
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "No text"}), 400
        
        if brain is None:
            return jsonify({"status": "error", "details": startup_error}), 500

        # AI gjen nese eshte kerkese per Web, Moti apo Muzike
        intent_data = brain.process(data['text'])
        response = router.route(intent_data)
        
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "error", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

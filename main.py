import os
import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

# Sigurohemi që folderi rrënjë është në path për importet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Variablat globalë për t'u përdorur në të gjithë serverin
brain = None
router = None
startup_error = "Sistemi po inicializohet..."

def init_all():
    """Inicializimi i të gjithë komponentëve të FalconAI"""
    global brain, router, startup_error
    try:
        print("--- Nisja e procesit të importimit ---")
        
        # Importet brenda funksionit për të izoluar gabimin
        from core.brain import FalconBrain
        from core.router import Router
        from engines.web_engine import WebEngine
        from engines.music_engine import MusicEngine
        from engines.weather_engine import WeatherEngine
        from engines.channels_engine import ChannelsEngine

        print("--- Krijimi i instancave të motorëve ---")
        web_engine = WebEngine()
        music_engine = MusicEngine()
        weather_engine = WeatherEngine()
        channels_engine = ChannelsEngine()

        print("--- Konfigurimi i Router-it ---")
        router = Router(
            music_engine=music_engine, 
            web_engine=web_engine, 
            weather_engine=weather_engine, 
            channels_engine=channels_engine
        )
        
        print("--- Ngarkimi i FalconBrain (ML Model) ---")
        # Këtu zakonisht dështon nëse pkl files mungojnë
        brain = FalconBrain()
        
        startup_error = "Success: Sistemi është gati."
        print("--- [SUCCESS] FalconAI u ngarkua plotësisht! ---")

    except Exception as e:
        # Kapim Stack Trace-in e plotë për debugging
        full_trace = traceback.format_exc()
        startup_error = f"GABIM: {str(e)}\n\nTRACEBACK:\n{full_trace}"
        print(f"!!! BOOT ERROR !!!\n{startup_error}")

# Thirrim inicializimin menjëherë pas definimit
init_all()

@app.route('/')
def health_check():
    """Ruta kryesore për të kontrolluar statusin nga Web-i"""
    return jsonify({
        "status": "online",
        "brain_ready": brain is not None,
        "router_ready": router is not None,
        "error_details": startup_error
    }), 200

@app.route('/process', methods=['POST'])
def process_request():
    """Ruta ku vijnë kërkesat nga Android TV"""
    global brain, router 
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400
        
        # Kontrollojmë nëse sistemi është gati
        if brain is None:
            return jsonify({
                "status": "error", 
                "message": "Brain is not ready", 
                "details": startup_error
            }), 500

        user_input = data['text']
        print(f"Processing query: {user_input}")

        # 1. Brain analizon tekstin (Intent Discovery)
        intent_data = brain.process(user_input)
        
        # 2. Router ekzekuton veprimin
        response = router.route(intent_data)
        
        # Sigurohemi që ka një status
        if 'status' not in response:
            response['status'] = 'success'
            
        return jsonify(response), 200

    except Exception as e:
        print(f"Request Error: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": "Internal processing error",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    # Konfigurimi i portit për Railway
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)

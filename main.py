import os
import sys
import traceback
from flask import Flask, request, jsonify
from flask_cors import CORS

# Sigurohemi që folderi rrënjë është në path për importet
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)
CORS(app)

# Variablat globalë
brain = None
router = None
startup_error = "Sistemi po inicializohet..."

def init_all():
    """Inicializimi i të gjithë komponentëve bazuar në strukturën tënde"""
    global brain, router, startup_error
    try:
        print("--- Nisja e inicializimit të FalconAI ---")
        
        # Importet nga folderat core dhe engines
        from core.brain import FalconBrain
        from core.router import Router
        from engines.web_engine import WebEngine
        from engines.music_engine import MusicEngine
        from engines.weather_engine import WeatherEngine

        # 1. Krijojmë motorët (Engines)
        web_engine = WebEngine()
        music_engine = MusicEngine()
        weather_engine = WeatherEngine()

        # 2. Inicializojmë Router-in (pa channels_engine siç ramë dakord)
        router = Router(
            music_engine=music_engine, 
            web_engine=web_engine, 
            weather_engine=weather_engine
        )
        
        # 3. Inicializojmë Trurin (ML Model)
        brain = FalconBrain()
        
        startup_error = "Success"
        print("--- [SUCCESS] Sistemi u ngarkua 100% ---")

    except Exception as e:
        full_trace = traceback.format_exc()
        startup_error = f"GABIM: {str(e)}\n\n{full_trace}"
        print(f"!!! BOOT ERROR !!!\n{startup_error}")

# Nisim procesin e inicializimit
init_all()

@app.route('/')
def health():
    """Kontrolli i statusit nga Browser-i"""
    is_ready = brain is not None and router is not None
    return jsonify({
        "status": "online",
        "brain_ready": brain is not None,
        "router_ready": router is not None,
        "system_status": "READY" if is_ready else "BOOTING/ERROR",
        "error_details": startup_error if not is_ready else "None"
    }), 200

@app.route('/process', methods=['POST'])
def process_request():
    """Pika kryesore e hyrjes për kërkesat nga Android TV"""
    global brain, router 
    
    try:
        data = request.get_json()
        
        # Kontrolli i të dhënave hyrëse
        if not data or 'text' not in data:
            return jsonify({"status": "error", "message": "No text provided"}), 400
        
        # Kontrolli nëse AI është gati
        if brain is None or router is None:
            return jsonify({
                "status": "error", 
                "message": "System not ready", 
                "details": startup_error
            }), 500

        user_input = data.get('text')
        # Marrim user_id nga kërkesa, ose përdorim një default për memorie
        user_id = data.get('user_id', 'default_user_tv')

        print(f"[*] Processing: '{user_input}' for user: {user_id}")

        # THIRRJA E TRURIT (Sipas brain.py: user_id, text, router)
        # Ky funksion bën: analyze -> router.route -> save_interaction -> kthen rezultatin
        result = brain.process(user_id=user_id, text=user_input, router=router)
        
        # Shtojmë një flag suksesi për frontend-in
        result['status'] = 'success'
            
        return jsonify(result), 200

    except Exception as e:
        print(f"Request Error: {str(e)}")
        return jsonify({
            "status": "error", 
            "message": "Internal processing error",
            "details": str(e),
            "trace": traceback.format_exc() if os.environ.get('DEBUG') else "Check logs"
        }), 500

if __name__ == "__main__":
    # Konfigurimi i portit për Railway (default 8080)
    port = int(os.environ.get("PORT", 8080))
    # Debug është false për siguri në produksion
    app.run(host='0.0.0.0', port=port, debug=False)
